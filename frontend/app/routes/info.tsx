import type { Route } from "./+types/home";

export const meta = ({}: Route.MetaArgs) => {
    return [
        { title: "New React Router App" },
        { name: "description", content: "Welcome to React Router!" },
    ];
};
const Info = () => {
    return <div>Hello Info</div>;
};

export default Info;
