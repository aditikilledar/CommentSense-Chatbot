/**
 * @file MUILanding.js is the landing page for the TA Chatbot stream
 * @author Sanjit Verma (skverma)
 */
import * as React from 'react';


import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import AppAppBar from './components/AppAppBar';
import Hero from './components/Hero';
import LogoCollection from './components/LogoCollection';
import Highlights from './components/Highlights';
import FAQ from './components/FAQ';
import Footer from './components/Footer';
import getLPTheme from './getLPTheme';

export default function LandingPage() {
  const [mode] = React.useState('dark');
  const LPtheme = createTheme(getLPTheme(mode));

  return (
    <ThemeProvider theme={LPtheme}>
      <div style={{ backgroundColor: 'rgb(20, 21, 21)' }}>
        <AppAppBar />
        <Hero />
        <Box sx={{ bgcolor: 'background.default' }}>
          <LogoCollection />
          <Divider />
          <Highlights />
          <Divider />
          <FAQ />
          <Divider />
          <Footer />
        </Box>
      </div>
    </ThemeProvider>

  );
}
