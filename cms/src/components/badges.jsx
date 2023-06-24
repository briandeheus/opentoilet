import React from "react"

function Badge({ children }) {
    return <span className="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-800 mr-1">
        {children}
    </span>
}
function BlueBadge({ children }) {
    return <span className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800 mr-1">
        {children}
    </span>
}

export { Badge, BlueBadge }