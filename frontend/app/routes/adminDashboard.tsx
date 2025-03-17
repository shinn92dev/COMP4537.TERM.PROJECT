import React, { useEffect, useState } from "react"
import { Users } from "lucide-react"

import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

interface AdminData {
    name: string
    email: string
}

interface User {
    id: number
    name: string
    email: string
    consumedAP: number
}

const adminDashboard = () => {
    const users: User[] = []

    return (
        <div className="p-6">
            <h1 className="text-3xl p-4">Admin Dashboard</h1>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Card className="p-4 shadow-lg">
                    <CardHeader className="flex justify-between items-center">
                        <CardTitle className="">Amin Information</CardTitle>
                        <Users className="w-5 h-5 text-gray-500" />
                    </CardHeader>
                    <CardContent className="flex items-center space-x-4">
                        <div>
                            <p className="">Name: </p>
                            <p className="">Email:</p>
                        </div>
                    </CardContent>
                </Card>
                <Card className="p-4 shadow-lg">
                    <CardHeader className="flex justify-between items-center">
                        <CardTitle>Remaining Requests</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-xl font-bold"># of remaining requests</p>
                        <CardDescription>You have requested # times so far</CardDescription>
                    </CardContent>
                </Card>
            </div>
            <Card className="mt-6 shadow-lg">
                <CardHeader>
                    <CardTitle>User AP Monitoring</CardTitle>
                    <CardDescription>
                    Here you can monitor user AP consumption.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    {users.length === 0 ? (
                    <div>No user data available.</div>
                    ) : (
                    users.map((user) => (
                        <div
                        key={user.id}
                        className="flex items-center justify-between py-2 border-b last:border-none"
                        >
                        <div className="flex items-center space-x-3">
                            <div>
                            <p className="font-medium">{user.name}</p>
                            <p className="text-sm text-muted-foreground">
                                {user.email}
                            </p>
                            </div>
                        </div>
            
                        <div className="text-sm font-medium">{user.consumedAP} AP</div>
                        </div>
                    ))
                    )}
                </CardContent>
            </Card>
        </div>
    )
}

export default adminDashboard
