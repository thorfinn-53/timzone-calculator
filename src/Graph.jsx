import React from 'react'
import { useEffect, useState } from "react"
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LabelList, CartesianGrid } from "recharts"
import { useNavigate } from "react-router-dom"

function getModColor(rank) {
  const rankColors = {
    "KNIGHT": "#ef4444",
    "VANGUARD_KNIGHT": "#f87171",
    "GENERAL": "#06b6d4",
    "SUPREME_GENERAL": "#22d3ee",
    "RECRUIT": "#eab308",
    "COMMANDER": "#dc2626",
    "PRIME_COMMANDER": "#b91c1c",
  }
  return rankColors[rank] || "#6b7280"
}

const RANK_GROUPS = {
  "KNIGHT": ["KNIGHT", "VANGUARD_KNIGHT"],
  "COMMANDER": ["COMMANDER", "PRIME_COMMANDER"],
  "GENERAL": ["GENERAL", "SUPREME_GENERAL"],
  "RECRUIT": ["RECRUIT"],
}

function transformData(rawData, activeMods) {
  return rawData.map(slot => {
    const entry = { time: `${Math.floor(slot.start_minute / 60)}:00` }
    activeMods.forEach(mod => {
      entry[mod] = slot.active_mods.includes(mod) ? 1 : 0
    })
    return entry
  })
}

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    const activeMods = payload.filter(p => p.value === 1)
    return (
      <div className="bg-white border border-gray-200 rounded-xl shadow-lg p-3 text-sm">
        <p className="font-semibold text-gray-700 mb-2">{label}</p>
        {activeMods.length === 0 ? (
          <p className="text-gray-400">No mods active</p>
        ) : (
          activeMods.map((p, i) => (
            <div key={i} className="flex items-center gap-2 mb-1">
              <div className="w-2.5 h-2.5 rounded-full" style={{ background: p.fill }} />
              <span className="text-gray-600">{p.dataKey}</span>
            </div>
          ))
        )}
      </div>
    )
  }
  return null
}

export default function Graph() {
  const [rawGraph, setRawGraph] = useState([])
  const [graphData, setGraphData] = useState([])
  const [allMods, setAllMods] = useState([])
  const [modRanks, setModRanks] = useState({})
  const [selectedMods, setSelectedMods] = useState([])
  const [selectedRanks, setSelectedRanks] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    async function fetchAll() {
      const [graphRes, modRes] = await Promise.all([
        fetch("http://127.0.0.1:8000/graph_data"),
        fetch("http://127.0.0.1:8000/moderators")
      ])
      const raw = await graphRes.json()
      const mods = await modRes.json()

      const rankMap = {}
      mods.forEach(mod => {
        rankMap[mod.name] = mod.rank.toUpperCase().replace(/ /g, "_")
      })
      setModRanks(rankMap)

      const modNames = [...new Set(raw.flatMap(slot => slot.active_mods))]
      setAllMods(modNames)
      setSelectedMods(modNames)
      setRawGraph(raw)
      setGraphData(transformData(raw, modNames))
    }
    fetchAll()
  }, [])

  // derive visible mods from BOTH filters independently
  const visibleMods = allMods.filter(mod => {
    const modSelected = selectedMods.includes(mod)
    const rankMatch = selectedRanks.length === 0 || selectedRanks.includes(modRanks[mod])
    return modSelected && rankMatch
  })

  useEffect(() => {
    if (rawGraph.length === 0) return
    setGraphData(transformData(rawGraph, visibleMods))
  }, [selectedMods, selectedRanks, rawGraph, modRanks])

  const toggleMod = (mod) => {
    setSelectedMods(prev =>
      prev.includes(mod) ? prev.filter(m => m !== mod) : [...prev, mod]
    )
  }

  const toggleRank = (groupName) => {
    const ranksInGroup = RANK_GROUPS[groupName]
    const allSelected = ranksInGroup.every(r => selectedRanks.includes(r))
    if (allSelected) {
      setSelectedRanks(prev => prev.filter(r => !ranksInGroup.includes(r)))
    } else {
      setSelectedRanks(prev => [...new Set([...prev, ...ranksInGroup])])
    }
  }

  const presentRankGroups = Object.keys(RANK_GROUPS).filter(group =>
    RANK_GROUPS[group].some(rank =>
      allMods.some(mod => modRanks[mod] === rank)
    )
  )

  return (
    <div className="min-h-screen bg-gray-50 px-8 py-10">

      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Moderator coverage</h1>
          <p className="text-sm text-gray-500 mt-1">Times shown in UTC</p>
        </div>
        <button
          onClick={() => navigate("/")}
          className="text-sm font-semibold text-indigo-600 border border-indigo-200 bg-indigo-50 px-4 py-2 rounded-lg hover:bg-indigo-100 transition cursor-pointer"
        >
          ← Back
        </button>
      </div>

      <div className="flex gap-6 mb-6">

        <div className="bg-white border border-gray-100 rounded-2xl shadow p-4 flex-1">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Filter by mod</p>
          <div className="flex flex-wrap gap-2">
            {allMods.map(mod => (
              <button
                key={mod}
                type="button"
                onClick={() => toggleMod(mod)}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border transition cursor-pointer ${
                  selectedMods.includes(mod)
                    ? "text-white border-transparent"
                    : "bg-white text-gray-400 border-gray-200"
                }`}
                style={selectedMods.includes(mod) ? { background: getModColor(modRanks[mod]), borderColor: getModColor(modRanks[mod]) } : {}}
              >
                {mod}
              </button>
            ))}
          </div>
        </div>

        <div className="bg-white border border-gray-100 rounded-2xl shadow p-4 flex-1">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Filter by rank</p>
          <div className="flex flex-wrap gap-2">
            {presentRankGroups.map(group => {
              const isActive = RANK_GROUPS[group].some(r => selectedRanks.includes(r))
              return (
                <button
                  key={group}
                  type="button"
                  onClick={() => toggleRank(group)}
                  className={`px-3 py-1 rounded-full text-xs font-medium border transition cursor-pointer ${
                    isActive ? "text-white border-transparent" : "bg-white text-gray-400 border-gray-200"
                  }`}
                  style={isActive ? { background: getModColor(group), borderColor: getModColor(group) } : {}}
                >
                  {group.replace(/_/g, " ")}
                </button>
              )
            })}
          </div>
        </div>

      </div>

      <div className="bg-white rounded-2xl border border-gray-100 shadow-xl p-6">
        <ResponsiveContainer width="100%" height={450}>
          <BarChart data={graphData} barCategoryGap={2} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
            <XAxis dataKey="time" tick={{ fontSize: 12, fill: "#6b7280" }} axisLine={{ stroke: "#e5e7eb" }} tickLine={false} />
            <YAxis allowDecimals={false} tick={{ fontSize: 12, fill: "#6b7280" }} axisLine={false} tickLine={false}
              label={{ value: "Mods active", angle: -90, position: "insideLeft", offset: 10, style: { fontSize: 12, fill: "#9ca3af" } }}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: "#f9fafb" }} />
            {visibleMods.map((mod) => (
              <Bar key={mod} dataKey={mod} stackId="a" fill={getModColor(modRanks[mod])} radius={[0, 0, 0, 0]}>
                <LabelList content={(props) => {
                  const { x, y, width, height } = props
                  if (height < 22) return null
                  return (
                    <text x={x + width / 2} y={y + height / 2} textAnchor="middle" dominantBaseline="middle" fill="white" fontSize={10} fontWeight={600}>
                      {mod}
                    </text>
                  )
                }} />
              </Bar>
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>

    </div>
  )
}