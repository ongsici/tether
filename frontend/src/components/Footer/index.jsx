import React from "react";
import { Box, Typography } from "@mui/material";
import "./Footer.css";

function Footer() {
  return (
    <Box className="footer">
      <Typography variant="body2">
        © {new Date().getFullYear()} TETHER. Background image from Adobe Stock Images. 
      </Typography>
    </Box>
  );
}

export default Footer;
