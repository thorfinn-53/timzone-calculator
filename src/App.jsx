import { useForm } from "react-hook-form";
import { ToastContainer, toast } from 'react-toastify';
import { Bounce } from "react-toastify";

export default function App() {

  const {
    register,
    handleSubmit,
    watch,
    reset,
    formState: { errors, isSubmitted },
  } = useForm();

  const onSubmit = (data) => {
    console.log(data)


    reset()

  }

  const showToast = () => {

    if (isSubmitted) {
      
      toast.success('Data submitted', {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "light",
        transition: Bounce,
      });
    }
  }





  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick={false}
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
        transition={Bounce}
      />

      <div className="w-full max-w-md space-y-8 rounded-2xl bg-white p-8 shadow-xl border border-gray-100">


        <div className="text-center">

          <h2 className="text-3xl font-bold tracking-tight text-gray-900">
            Fill out the details
          </h2>
          <p className="mt-2 text-sm text-gray-500">
            Please fill out the information below.
          </p>
        </div>

        {/* Form */}
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <div className="space-y-5">

            {/* Name Input */}
            <div className="flex flex-col gap-1.5">
              <label htmlFor="Name" className="text-sm font-semibold text-gray-700">
                Name
              </label>
              <input
                id="Name"
                type="text"
                placeholder="Name"
                className={`w-full rounded-lg border px-4 py-2.5 text-gray-900 placeholder-gray-400 shadow-sm transition duration-200 focus:outline-none focus:ring-2 ${errors.Name
                  ? "border-red-300 focus:border-red-500 focus:ring-red-200"
                  : "border-gray-300 focus:border-indigo-500 focus:ring-indigo-100"
                  }`}
                {...register("Name", {
                  required: { value: true, message: "This field is required" },
                  minLength: { value: 4, message: "Minimum length should be 4" },
                  maxLength: { value: 20, message: "Maximum length is 20" },
                  pattern: { value: /^[A-Za-z\s]+$/, message: "Name should only contain letters" }, // Allowed spaces for full names
                })}
              />
              {errors.Name && (
                <span className="text-xs font-medium text-red-500 animate-fadeIn">
                  {errors.Name.message}
                </span>
              )}
            </div>

            {/* Rank Input */}
            <div className="flex flex-col gap-1.5">
              <label htmlFor="Rank" className="text-sm font-semibold text-gray-700">
                Rank
              </label>
              <input
                id="Rank"
                type="text"
                placeholder="e.g. Knight"
                className={`w-full rounded-lg border px-4 py-2.5 text-gray-900 placeholder-gray-400 shadow-sm transition duration-200 focus:outline-none focus:ring-2 ${errors.Rank
                  ? "border-red-300 focus:border-red-500 focus:ring-red-200"
                  : "border-gray-300 focus:border-indigo-500 focus:ring-indigo-100"
                  }`}
                {...register("Rank", {
                  required: { value: true, message: "This field is required" },
                  minLength: { value: 4, message: "Minimum length should be 4" },
                  maxLength: { value: 20, message: "Maximum length is 20" },
                  pattern: { value: /^[A-Za-z]+$/, message: "Rank should only contain letters" },
                })}
              />
              {errors.Rank && (
                <span className="text-xs font-medium text-red-500">
                  {errors.Rank.message}
                </span>
              )}
            </div>

            {/* Timezone Input */}
            <div className="flex flex-col gap-1.5">
              <label htmlFor="Timezone" className="text-sm font-semibold text-gray-700">
                Timezone
              </label>
              <input
                id="Timezone"
                type="text"
                placeholder="e.g. EST"
                className={`w-full rounded-lg border px-4 py-2.5 text-gray-900 placeholder-gray-400 shadow-sm transition duration-200 focus:outline-none focus:ring-2 ${errors.Timezone
                  ? "border-red-300 focus:border-red-500 focus:ring-red-200"
                  : "border-gray-300 focus:border-indigo-500 focus:ring-indigo-100"
                  }`}
                {...register("Timezone", {
                  required: { value: true, message: "This field is required" },
                  minLength: { value: 2, message: "Minimum length should be 2" },
                  maxLength: { value: 20, message: "Maximum length is 20" },

                })}
              />
              {errors.Timezone && (
                <span className="text-xs font-medium text-red-500">
                  {errors.Timezone.message}
                </span>
              )}
              <label htmlFor="Availability">Availability</label>

              <input
                id="start"
                type="time"

                className={`w-full rounded-lg border px-4 py-2.5 text-gray-900 placeholder-gray-400 shadow-sm transition duration-200 focus:outline-none focus:ring-2 ${errors.Timezone
                  ? "border-red-300 focus:border-red-500 focus:ring-red-200"
                  : "border-gray-300 focus:border-indigo-500 focus:ring-indigo-100"
                  }`}
                {...register("startTime", {
                  required: { value: true, message: "This field is required" },


                })}
              />
              {errors.startTime && (
                <span className="text-xs font-medium text-red-500">
                  {errors.startTime.message}
                </span>
              )}

              <input
                id="end"
                type="time"

                className={`w-full rounded-lg border px-4 py-2.5 text-gray-900 placeholder-gray-400 shadow-sm transition duration-200 focus:outline-none focus:ring-2 ${errors.Timezone
                  ? "border-red-300 focus:border-red-500 focus:ring-red-200"
                  : "border-gray-300 focus:border-indigo-500 focus:ring-indigo-100"
                  }`}
                {...register("endTime", {
                  required: { value: true, message: "This field is required" },


                })}
              />
              {errors.endTime && (
                <span className="text-xs font-medium text-red-500">
                  {errors.endTime.message}
                </span>
              )}







            </div>

          </div>

          {/* Submit Button */}
          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-lg bg-indigo-600 px-4 py-3 text-sm font-semibold text-white shadow-md transition duration-200 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 active:bg-indigo-800 cursor-pointer"
              onClick={showToast}
            >
              Submit
            </button>
          </div>
        </form>

      </div>
    </div>
  );
}