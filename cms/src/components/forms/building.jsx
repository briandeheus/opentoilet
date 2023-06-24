import { useCallback, Fragment } from "react";
import FormInput from "../form-input";
import api from "../../utils/api";
import { useStore } from "../../store";
import { PrimaryButton } from "../buttons";

export default function BuildingForm() {

    const [
        building,
        updateBuilding,
    ] = useStore(state => [
        state.building,
        state.updateBuilding,
    ]);

    const saveBuilding = useCallback(async () => {

        const [res, statusCode] = await api.post("/api/v1/buildings/", building);

    }, [building]);

    if (building === null) {
        return <div></div>
    }

    return <Fragment>
        <FormInput
            label="Building Name"
            placeholder="OpenToilet Tower"
            value={building.name}
            onChange={(value) => updateBuilding("name", value)}
        />
        <FormInput
            label="Latitude"
            value={building.latlng[0]}
            disabled
        />
        <FormInput
            label="Longitude"
            value={building.latlng[1]}
            disabled
        />
        <PrimaryButton onClick={saveBuilding}>Save</PrimaryButton>
    </Fragment>

}