import React, { Fragment, useEffect } from "react";
import { Link } from "wouter";
import { Table, TableHeader, TableRow, TableColumn } from "../../components/table";
import { useStore } from "../../store";

export default function AmenitiesList() {
    const [
        amenities,
        getAmenities,
    ] = useStore(state => [
        state.amenities,
        state.getAmenities
    ]);

    useEffect(() => {
        getAmenities();
    }, []);

    return (
        <Fragment>
            <div className="sm:flex sm:items-center">
                <div className="sm:flex-auto">
                    <h1 className="text-base font-semibold leading-2 text-gray-900">Amenities</h1>
                </div>
                <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
                    <Link to="/amenities/new">
                        <button
                            type="button"
                            className="block rounded-md bg-indigo-600 py-2 px-3 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                        >
                            Add Amenity
                        </button>
                    </Link>
                </div>
            </div>
            <Table
                headers={[
                    <TableHeader key="name">Name</TableHeader>,
                    <TableHeader key="edit"></TableHeader>
                ]}
                rows={[
                    amenities.map(a => <TableRow key={a.id}>
                        <TableColumn>
                            <div className="font-medium">{a.name}</div>
                        </TableColumn>
                        <TableColumn>
                            <Link to={`/amenities/${a.id}/`}>
                                <a href="#" className="font-medium text-indigo-600 hover:text-indigo-900">
                                    Update
                                </a>
                            </Link>
                        </TableColumn>
                    </TableRow>)
                ]}
            />
        </Fragment>
    );

}