import React from "react";

function TableRow({ children }) {
    return <tr>
        {children}
    </tr>
}

function TableColumn({ children }) {
    return <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm sm:pl-6 align-top">
        {children}
    </td>
}

function TableHeader({ children }) {
    return <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
        {children}
    </th>
}

function Table({ headers, rows }) {
    return <div className="mt-8 flow-root">
        <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
                    <table className="min-w-full divide-y divide-gray-300 ">
                        <thead className="bg-gray-50">
                            <tr>
                                {headers}
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200 bg-white">
                            {rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
}

export { Table, TableHeader, TableRow, TableColumn }