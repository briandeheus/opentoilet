import { useCallback, Fragment, useEffect, useState } from "react";
import FormInput from "../form-input";
import api from "../../utils/api";
import { useStore } from "../../store";
import { PrimaryButton } from "../buttons";

class FormField {

    constructor({ label, key, value, placeholder = "", disabled = false }) {
        this.label = label;
        this.key = key;
        this.value = value;
        this.placeholder = placeholder
        this.disabled = disabled
    }

}

export default function BaseForm({ fields, onSave }) {

    const [fieldValues, setFieldValues] = useState({});

    useEffect(() => {

        const newValues = {}
        fields.forEach(f => newValues[f.key] = f.value);
        setFieldValues(newValues);

    }, [fields]);

    const updateField = useCallback((key, value) => {

        fieldValues[key] = value;
        setFieldValues({ ...fieldValues });

    }, [fieldValues]);

    return <Fragment>
        {fields.map((f, i) => {
            return <FormInput key={f.key}
                label={f.label}
                placeholder={f.placeholder}
                value={fieldValues[f.key]}
                onChange={(value) => updateField(f.key, value)}
            />
        })}
        <PrimaryButton onClick={() => onSave(fieldValues)}>Save</PrimaryButton>
    </Fragment>

}

export { FormField }