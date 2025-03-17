import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    route("register", "routes/register.tsx"),
    route("info", "routes/info.tsx"),
    route("userDashboard", "routes/userDashboard.tsx"),
    route("adminDashboard", "routes/adminDashboard.tsx"),
    route("login", "routes/login.tsx")
] satisfies RouteConfig;
