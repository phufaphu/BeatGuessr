import './app.css';
import { mount } from 'svelte';
import Home from './lib/pages/Home.svelte'
import About from './lib/pages/About.svelte'

const homeEl = document.getElementById('home-app');
if (homeEl) {
  mount(Home, {
    target: homeEl,
  });
}

const aboutEl = document.getElementById('about-app');
if (aboutEl) {
  mount(About, {
    target: aboutEl,
  });
}