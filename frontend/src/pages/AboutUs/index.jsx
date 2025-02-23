import { Container, Typography } from "@mui/material"
import "./AboutUs.css";

function AboutUs () {
  return (
    <Container maxWidth="md" sx={{ mt: 6, textAlign: "center" }} className="home-container">
      <div className="background-overlay"></div>
      <Typography variant="h2" className="welcome-title">About Us</Typography>
    </Container>
   );
}

export default AboutUs;