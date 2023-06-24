import { Warning } from "postcss";
import React, { Fragment, useCallback, useEffect, useState } from "react";
import { Link } from "wouter";
import { Badge, BlueBadge } from "../../components/badges";
import Breadcrumbs from "../../components/bradcrumbs";
import { PrimaryButton, SecondaryButton, WarningButton } from "../../components/buttons";
import FormInput from "../../components/form-input";
import RestroomForm from "../../components/forms/restroom";
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

export default function FloorsSingle({ id }) {

    const [floor, setFloor] = useState(null);
    const [modalOpen, setModalOpen] = useState(false);

    const loadFloor = useCallback(async () => {

        const [fRes, fStatusCode] = await api.get(`/api/v1/floors/${id}`);
        setFloor(fRes);

    }, [id]);

    useEffect(() => {

        loadFloor();

    }, [id]);

    if (floor === null) {
        return <div>Loading...</div>
    }

    const building = floor.building;
    const pages = [
        { name: 'Buildings', href: '/buildings', current: false },
        { name: building.name, href: `/buildings/${building.id}`, current: false },
        { name: `Floor ${floor.floor_number}`, href: `/buildings/${building.id}/floors/${id}`, current: true }
    ]

    return (
        <Fragment>
            <Modal
                visible={modalOpen}
                onClose={() => { setModalOpen(false) }}
            >
                <div>
                    <P>
                        Use this form to add a new restroom on floor {floor.floor_number} of <strong>{building.name}</strong>. After you add a restroom, you can configure the restroom with toilet types and amenities.
                    </P>
                </div>
                <RestroomForm />
            </Modal>
            <div className="sm:flex sm:items-center">
                <div className="sm:flex-auto">
                    <h1 className="text-base font-semibold leading-2 text-gray-900">{building.name} - Floor {floor.floor_number}</h1>
                </div>
                <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
                    <PrimaryButton
                        onClick={() => setModalOpen(true)}
                    >
                        Add Restroom
                    </PrimaryButton>
                </div>
            </div>
            <Breadcrumbs pages={pages} />
            <Table
                headers={[
                    <TableHeader key="name">Gender</TableHeader>,
                    <TableHeader key="genders">Types</TableHeader>,
                    <TableHeader key="amenities">Amenities</TableHeader>,
                    <TableHeader key="edit"></TableHeader>
                ]}
                rows={[
                    floor.restrooms.map((r) => {

                        return <TableRow key={r.id}>
                            <TableColumn>
                                <div className="font-medium capitalize">{r.gender}</div>
                            </TableColumn>
                            <TableColumn>
                                {r.toilet_types.map(t => <Badge key={t.name}>{t.name} {t.count}x</Badge>)}
                            </TableColumn>
                            <TableColumn>
                                {r.amenities.map(a => <Badge key={a.id}>{a.name}</Badge>)}
                            </TableColumn>
                            <TableColumn>
                                <Link to={`/buildings/${building.id}/floors/${r.id}`}>
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
