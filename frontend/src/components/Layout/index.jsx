// import { useState } from "react";
import { Outlet } from "react-router-dom";

import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";

export default function Layout() {
//   const [isUploadDialogOpen, setIsUploadDialogOpen] = useState(false);

//   const handleUpload = () => {
//     setIsUploadDialogOpen(true);
//   };

//   const handleDialogClose = () => {
//     setIsUploadDialogOpen(false);
//   };

  return (
    <>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="fixed" sx={{ top: 0, width: "100%" }}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Welcome to Tether!
            </Typography>
          </Toolbar>
        </AppBar>
      </Box>

      <Outlet />
    </>
  );
}