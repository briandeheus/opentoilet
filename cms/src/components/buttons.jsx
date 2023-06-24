import React from "react"

const PrimaryButton = ({ onClick, children }) => {
    return (
        <button
            onClick={onClick}
            type="button"
            className="rounded-md bg-indigo-600 py-1.5 px-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
        >
            {children}
        </button>
    )
}

const SecondaryButton = ({ onClick, children }) => {
    return (
        <button
            onClick={onClick}
            type="button"
            className="rounded-md bg-white py-1.5 px-2.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
        >
            {children}
        </button>
    )
}

const WarningButton = ({ onClick, children }) => {
    return (<button
        type="button"
        className="rounded-md py-1.5 px-2.5 text-sm font-semibold shadow-sm bg-red-600 text-white shadow-sm hover:bg-red-500"
        onClick={onClick}
    >
        {children}
    </button>)
}




export { PrimaryButton, SecondaryButton, WarningButton }