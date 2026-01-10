const BASE_URL = 'http://localhost:8080';

export const registrarUsuario = async (novoUsuario) => {
    // eslint-disable-next-line no-useless-catch
    try {
        const response = await fetch(`${BASE_URL}/usuarios/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(novoUsuario)
        });
        return response;
    } catch (error) {
        throw error;
    }
};

export const loginUsuario = async (credenciais) => {
    // eslint-disable-next-line no-useless-catch
    try {
        const response = await fetch(`${BASE_URL}/usuarios/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credenciais)
        });
        return response;
    } catch (error) {
        throw error;
    }
};