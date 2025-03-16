import axios from "axios"

const API_BASE_URL = "http://localhost:8000";

export const login = async (prevState: string | null, formData: FormData) => {
    // Convert FormData to URLSearchParams for FastAPI OAuth2 compatibility
    const username = formData.get("email") as string;
    const password = formData.get("password") as string;
    
    if (!username || !password) {
        return "Email and password are required";
    }
    
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);

    try {
        const res = await axios.post(`${API_BASE_URL}/auth/token`, params, {
            withCredentials: true,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            }
        });

        if (res.data.status === 200) {
            // Return a success flag that the component can use to navigate
            return { success: true };
        }
        
        return null;
    } catch (error: any) {
        console.error(error);
        if (error.response?.data?.detail) {
            return error.response.data.detail;
        }
        return "Login failed. Please try again.";
    }  
}
