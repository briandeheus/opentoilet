import React, { useCallback, useState } from "react";
import { PrimaryButton } from "../components/buttons";
import FormInput from "../components/form-input";
import { useStore } from "../store";
import api from "../utils/api";

export default function LoginView() {

    const [setApiToken, setView] = useStore(state => [state.setApiToken, state.setView]);

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const login = useCallback(async () => {
        const [res, statusCode] = await api.post("/api/v1/account/login", { username, password });

        if (statusCode !== 200) {
            setError("Incorrect username or password.");
            return;
        }

        setApiToken(res.token);

    }, [username, password]);

    return <div className="min-h-screen flex items-center justify-center">
        <div className="pt-8 rounded w-96">
            <h2 className="text-2xl font-bold mb-6">Opentoilet CMS</h2>
            <FormInput label="Username" placeholder="john@opentoilet.xyz" id="username" onChange={setUsername} value={username} />
            <FormInput label="Password" placeholder="********" id="password" type="password" onChange={setPassword} value={password} />
            <div className='pt-5'>
                <PrimaryButton onClick={login}>Sign In</PrimaryButton>
            </div>
        </div>
    </div>
}