export const register =  async (data: Object)=> {
    try{
        const res = await fetch("https://bcit-anthony-sh-s.com/lumisenseai/api/v1/register",
            {
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            }
        )
        const result = await res.json();

        if (res.ok){
            return {success: true, message: result.message || "Registration successful"}
        } else {
            return {success: false, error: result.message || "Unknown error"}
        }
    }
    catch (error){
        return {success: false, error: error || "Network or unknown error"}
    }
}