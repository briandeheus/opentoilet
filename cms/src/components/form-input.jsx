import "react";

export default function FormInput({ label, id, onChange, type = "text", value = "", placeholder = "", disabled = false, error = null }) {
    return <div className="py-2">
        <label htmlFor={id} className="block text-sm font-medium leading-6 text-gray-900">
            {label}
        </label>
        <div className="relative mt-1 rounded-md shadow-sm">
            <input
                onChange={({ target }) => onChange(target.value)}
                type={type}
                id={id}
                disabled={disabled}
                className={`block w-full rounded-md border-0 py-1.5 pr-10 ring-1 ring-inset focus:ring-2 focus:ring-inset ${error ? "text-red-900 ring-red-300 placeholder:text-red-300 focus:ring-red-500" : ""}`}
                placeholder={placeholder}
                value={value}
            />
            {error &&
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                    <ExclamationCircleIcon className="h-5 w-5 text-red-500" aria-hidden="true" />
                </div>
            }
        </div>
        {error &&
            <p className="mt-2 text-sm text-red-600">
                {{ error }}
            </p>
        }
    </div>
}