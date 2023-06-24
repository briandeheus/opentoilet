import React, { Fragment, useCallback, useEffect, useState } from "react";
import BaseForm, { FormField } from "../../components/forms/base";
import { Table, TableHeader, TableRow, TableColumn } from "../../components/table";
import { useStore } from "../../store";
import api from "../../utils/api";

export default function AmenitiesSingle({ id }) {

    const [
        amenities
    ] = useStore(state => [
        state.amenities
    ]);

    const [amenity, setAmenity] = useState({});

    const onSave = useCallback(async (values) => {

        if (id === "new") {
            const [res, statusCode] = await api.post("/api/v1/amenities", values);
        } else {
            const [res, statusCode] = await api.put(`/api/v1/amenities/${id}`, values);
        }

    }, [id]);

    useEffect(() => {

        if (id === "new") {
            return;
        }

        (async () => {

            const [res, statusCode] = await api.get(`/api/v1/amenities/${id}`);
            setAmenity(res);

        })();

    }, [id]);

    return (
        <Fragment>
            <BaseForm
                fields={[
                    new FormField({ label: "Name", key: "name", placeholder: "Toiletpaper", value: amenity.name })
                ]}
                onSave={onSave}
            />
        </Fragment>
    );

}