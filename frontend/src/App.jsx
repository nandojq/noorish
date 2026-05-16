import { Routes, Route, Navigate } from "react-router-dom";
import AppShell from "@/components/layout/AppShell";
import MenuPlanner from "@/views/MenuPlanner/index";
import RecipeLibrary from "@/views/RecipeLibrary";
import RecipeDetail from "@/views/RecipeDetail";
import RecipeForm from "@/views/RecipeForm";
import IngredientDatabase from "@/views/IngredientDatabase";
import NutritionAnalysis from "@/views/NutritionAnalysis";
import GroceryList from "@/views/GroceryList";
import Settings from "@/views/Settings";

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<Navigate to="/menus" replace />} />
        <Route path="/menus" element={<MenuPlanner />} />
        <Route path="/menus/:id" element={<MenuPlanner />} />
        <Route path="/recipes" element={<RecipeLibrary />} />
        <Route path="/recipes/new" element={<RecipeForm />} />
        <Route path="/recipes/:id" element={<RecipeDetail />} />
        <Route path="/recipes/:id/edit" element={<RecipeForm />} />
        <Route path="/ingredients" element={<IngredientDatabase />} />
        <Route path="/analysis/:menuId" element={<NutritionAnalysis />} />
        <Route path="/grocery/:menuId" element={<GroceryList />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </AppShell>
  );
}
