import { Warning } from "postcss";
import React, { Fragment, useCallback, useEffect, useState } from "react";
import { Link } from "wouter";
import { Badge, BlueBadge } from "../../components/badges";
import Breadcrumbs from "../../components/bradcrumbs";
import { PrimaryButton, SecondaryButton, WarningButton } from "../../components/buttons";
import FormInput from "../../components/form-input";
import Modal from "../../components/modal";
import P from "../../components/paragraph";
import { Table, TableColumn, TableHeader, TableRow } from "../../components/table";

import { useStore } from "../../store";
import api from "../../utils/api";

const capitalizeFirstLetter = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
};

const getRestrooms = (floor) => {

    const genders = {}

    floor.restrooms.forEach(({ gender, toilet_types: toiletTypes }) => {

        if (genders[gender] === undefined) {
            genders[gender] = {}
        }

        toiletTypes.forEach(({ name, count }) => {

            if (genders[gender][name] === undefined) {
                genders[gender][name] = 0;
            }

            genders[gender][name] += count

        });

    });

    return genders

}

export default function BuildingsSingle({ id }) {

    const [floors, setFloors] = useState([]);
    const [building, setBuilding] = useState(null);
    const [modalOpen, setModalOpen] = useState(false);
    const [floorNumber, setFloorNumber] = useState(1);

    const loadBuilding = useCallback(async () => {

        const [fRes, fStatusCode] = await api.get("/api/v1/floors/", { building: id });
        setFloors(fRes.results);

        const [bRes, bStatusCode] = await api.get(`/api/v1/buildings/${id}/`);
        setBuilding(bRes);

        setFloorNumber(fRes.results.length + 1);

    }, [id]);

    const addFloor = useCallback(async () => {

        const [res, statusCode] = await api.post("/api/v1/floors/", { building: building.id, floor_number: floorNumber });
        loadBuilding();
        setModalOpen(false);

    }, [building, floorNumber]);

    useEffect(() => {

        loadBuilding();

    }, [id]);

    if (building === null) {
        return <div>Loading...</div>
    }

    const pages = [
        { name: 'Buildings', href: '/buildings', current: false },
        { name: building.name, href: `/buildings/${building.id}`, current: true }
    ]

    return (
        <Fragment>
            <Modal
                visible={modalOpen}
                onClose={() => { setModalOpen(false) }}
            >
                <div>
                    <P>
                        Use this form to add a new floor to <strong>{building.name}</strong>. After you add a floor, you can add restrooms to the newly created floor.
                    </P>
                    <FormInput
                        label="Floor Number"
                        type="number"
                        placeholder="1"
                        value={floorNumber}
                        onChange={(f) => setFloorNumber(parseInt(f))}
                    />
                </div>
                <div className="mt-2 flex-row-reverse flex flex-wrap gap-1">
                    <PrimaryButton onClick={addFloor}>
                        Save
                    </PrimaryButton>
                    <SecondaryButton onClick={() => setModalOpen(false)}>
                        Cancel
                    </SecondaryButton>
                </div>
            </Modal>
            <div className="sm:flex sm:items-center">
                <div className="sm:flex-auto">
                    <h1 className="text-base font-semibold leading-2 text-gray-900">{building.name}</h1>
                </div>
                <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
                    <PrimaryButton
                        onClick={() => setModalOpen(true)}
                    >
                        Add Floor
                    </PrimaryButton>
                </div>
            </div>
            <Breadcrumbs pages={pages} />
            <Table
                headers={[
                    <TableHeader key="name">Floor</TableHeader>,
                    <TableHeader key="genders">Restrooms</TableHeader>,
                    <TableHeader key="edit"></TableHeader>
                ]}
                rows={[
                    floors.map((f) => {

                        const restrooms = getRestrooms(f);
                        const genders = Object.keys(restrooms);

                        return <TableRow key={f.id}>
                            <TableColumn>
                                <div className="font-medium">Floor {f.floor_number}</div>
                            </TableColumn>
                            <TableColumn>
                                {genders.map(g => {
                                    const toiletTypes = Object.keys(restrooms[g]);
                                    return (<div className="pb-2" key={g}>
                                        <div className="font-medium capitalize pb-1">
                                            {g}
                                        </div>
                                        {toiletTypes.map(t => <Badge key={t}>{t} {restrooms[g][t]}x</Badge>)}
                                    </div>
                                    )
                                })}
                            </TableColumn>
                            <TableColumn>
                                <Link to={`/buildings/${building.id}/floors/${f.id}`}>
                                    <a href="#" className="font-medium text-indigo-600 hover:text-indigo-900">
                                        View
                                    </a>
                                </Link>
                            </TableColumn>
                        </TableRow>
                    })
                ]}
            />
        </Fragment>
    );

}
