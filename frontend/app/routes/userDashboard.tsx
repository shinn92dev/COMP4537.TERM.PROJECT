import React, { useEffect, useState } from "react";
import { Users, CheckCircle, Circle } from "lucide-react";

import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

interface UserData {
    remainingRequests: number;
    requestLimit: number;
    email: string;
    name: string;
}


const userDashboard = () => {
    const [userData, setUserData] = useState<UserData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    
    useEffect(() => {
        fetch("http://localhost:8000/user-dashboard/user-info", {
            credentials: "include",
            mode: "cors"
        })
        .then((res) => res.json())
        .then((data) => setUserData(data))
        .catch((err) => console.log("Error", err))
    })


    return (
        <div className="p-6">
            <h1 className="text-3xl p-4">User Dashboard</h1>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Card className="p-4 shadow-lg">
                    <CardHeader className="flex justify-between items-center">
                        <CardTitle className="">User Information</CardTitle>
                        <Users className="w-5 h-5 text-gray-500" />
                    </CardHeader>
                    <CardContent className="flex items-center space-x-4">
                        <div>
                            <p className="">Name: {userData?.name}</p>
                            <p className="">Email: {userData?.email}</p>
                        </div>
                    </CardContent>
                </Card>
                <Card className="p-4 shadow-lg">
                    <CardHeader className="flex justify-between items-center">
                        <CardTitle>Remaining Requests</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-2xl font-bold">{userData?.remainingRequests}</p>
                        <CardDescription>You have requested # times so far</CardDescription>
                    </CardContent>
                </Card>
            </div>
        </div>
        
    )
};

export default userDashboard;