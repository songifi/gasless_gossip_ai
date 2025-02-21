import ThemeSwitcher from "./ThemeSwitcher";

export default function Navbar() {
  return (
    <nav className="p-4 bg-base-200 flex justify-between items-center">
      <h1 className="text-xl font-bold">Gasless</h1>
      <ThemeSwitcher />
    </nav>
  );
}
