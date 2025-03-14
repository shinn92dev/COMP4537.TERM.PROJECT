import React, { useEffect, useState } from "react";

interface DashboardData {
    remainingRequests: number;
}


const Dashboard = () => {
    const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    return (
        <section className="p-6">
            <h1 className="text-xl font-bold mb-4">Dashboard</h1>
            <p>Remaining API calls:</p>
        </section>
    )
};

export default Dashboard;