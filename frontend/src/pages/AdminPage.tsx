import React from "react";
import { Admin, Resource } from "react-admin";
import simpleRestProvider from "ra-data-simple-rest";

const AdminPage: React.FC = () => {
  const dataProvider = simpleRestProvider("http://localhost:8000/api");
  return (
    <Admin dataProvider={dataProvider} basename="/admin">
      <Resource name="users" />
      <Resource name="plans" />
      <Resource name="subscriptions" />
      <Resource name="tasks" />
      <Resource name="knowledge" />
    </Admin>
  );
};

export default AdminPage;
