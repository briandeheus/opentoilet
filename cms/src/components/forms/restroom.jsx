import { useCallback, Fragment, useEffect, useState } from "react";
import FormInput from "../form-input";
import api from "../../utils/api";
import { useStore } from "../../store";
import { PrimaryButton, SecondaryButton } from "../buttons";
import FormSelect from "../form-select";

export default function RestroomForm() {

    const [genders, setGenders] = useState([]);
    const [amenities, setAmenities] = useState([]);
    const [toiletTypes, setToiletTypes] = useState([]);

    useEffect(() => {

        (async () => {

            const [g, gs] = await api.get("/api/v1/genders");
            setGenders(g);

            const [a, as] = await api.get("/api/v1/amenities");
            setAmenities(a.results);

            const [t, ts] = await api.get("/api/v1/toilet-types");
            setToiletTypes(t.results);

        })();

    }, []);


    return <Fragment>
        <div>
            <FormSelect
                label="Gender"
                value={genders[0]}
                values={genders.map(g => { return { value: g, label: g } })}
            />
            <div className="block text-sm font-medium leading-6 text-gray-900 my-2">
                Toilet Types
            </div>
            <div>
                {toiletTypes.map(t => {
                    return <div className="grid grid-cols-2 gap-4 mb-1">
                        <div className="col-span-1 text-sm">
                            {t.name}
                        </div>
                        <div className="col-span-1">
                            <input
                                onChange={({ target }) => onChange(target.value)}
                                type="number"
                                className={`w-full rounded-md border-0 py-1.5 ring-1 ring-inset focus:ring-2 focus:ring-inset text-sm`}
                                value={0}
                            />
                        </div>
                    </div>
                })}
            </div>
            <fieldset className="my-2">
                <div className="block text-sm font-medium leading-6 text-gray-900">
                    Amenities
                </div>
                {amenities.map(a => {
                    return <div className="space-y-5" key={a.id}>
                        <div className="relative flex items-start">
                            <div className="flex h-6 items-center">
                                <input
                                    id={`a${a.id}`}
                                    aria-describedby="comments-description"
                                    name="comments"
                                    type="checkbox"
                                    className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600"
                                />
                            </div>
                            <div className="ml-3 text-sm leading-6">
                                <label htmlFor={`a${a.id}`} className="text-gray-900">
                                    {a.name}
                                </label>
                            </div>
                        </div>
                    </div>
                })}

            </fieldset>
        </div>
        <div className="mt-2 flex-row-reverse flex flex-wrap gap-1">
            <PrimaryButton onClick={() => { }}>
                Save
            </PrimaryButton>
            <SecondaryButton onClick={() => setModalOpen(false)}>
                Cancel
            </SecondaryButton>
        </div>
    </Fragment>

}