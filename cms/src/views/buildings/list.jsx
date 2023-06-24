import React, { Fragment, useEffect } from "react";
import { Link } from "wouter";
import Breadcrumbs from "../../components/bradcrumbs";
import { Table, TableColumn, TableHeader, TableRow } from "../../components/table";

import { useStore } from "../../store";

const pages = [
    { name: 'Buildings', href: '/buildings', current: true },
]

export default function BuildingsList() {

    const [
        buildings,
        getBuildings,
    ] = useStore(state => [
        state.buildings,
        state.getBuildings
    ]);

    useEffect(() => {

        getBuildings();

    }, []);

    return (
        <Fragment>
            <div className="sm:flex sm:items-center">
                <div className="sm:flex-auto">
                    <h1 className="text-base font-semibold leading-2 text-gray-900">Buildings</h1>
                </div>
                <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
                    <button
                        type="button"
                        className="block rounded-md bg-indigo-600 py-2 px-3 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                    >
                        Add Building
                    </button>
                </div>
            </div>
            <div>
                <Breadcrumbs pages={pages} />
            </div>
            <Table
                headers={[
                    <TableHeader key="name">Name</TableHeader>,
                    <TableHeader key="edit"></TableHeader>
                ]}
                rows={[
                    buildings.map(b => <TableRow key={b.id}>
                        <TableColumn>
                            <div className="font-medium">{b.name}</div>
                            <div className="text-gray-600">{b.toilet_count} toilets</div>
                        </TableColumn>
                        <TableColumn>
                            <Link to={`/buildings/${b.id}/`}>
                                <a href="#" className="font-medium text-indigo-600 hover:text-indigo-900">
                                    View
                                </a>
                            </Link>
                        </TableColumn>
                    </TableRow>)
                ]}
            />
        </Fragment>
    );

}