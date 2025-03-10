import type { Route } from "./+types/home";

export const meta = ({}: Route.MetaArgs) => {
    return [
        { title: "New React Router App" },
        { name: "description", content: "Welcome to React Router!" },
    ];
};

const Home = () => {
    return <div>HOME</div>;
};

export default Home;
