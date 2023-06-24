export default function FormSelect({ label, values, value }) {
    return <div>
        <label htmlFor={label} className="block text-sm font-medium leading-6 text-gray-900">
            {label}
        </label>
        <select
            id={label}
            className="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6"
            value={value}
        >
            {values.map(v => <option key={v.value} value={v.value}>{v.label}</option>)}
        </select>
    </div>
}