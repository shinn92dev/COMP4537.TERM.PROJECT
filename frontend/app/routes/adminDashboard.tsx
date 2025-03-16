import React, { useEffect, useState } from "react";

interface AdminDashboardData {
    users: {
        email: string;
        remainingRequests: number;
        requestLimit: number;
    }[];
}

const AdminDashboard = () => {
    const [adminData, setAdminData] = useState<AdminDashboardData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
}