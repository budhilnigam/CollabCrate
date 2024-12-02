<template>
  <div class="min-vh-100 d-flex flex-column bg-light">
    <!-- Header -->
    <header class="bg-primary text-white py-3">
      <div class="container d-flex justify-content-between align-items-center">
        <h1 class="h3">SponsorLink</h1>
        <nav>
          <ul class="nav">
            <li class="nav-item">
              <a href="#about" class="nav-link text-white">About</a>
            </li>
            <li class="nav-item">
              <a href="#features" class="nav-link text-white">Features</a>
            </li>
            <li class="nav-item">
              <a href="#contact" class="nav-link text-white">Contact</a>
            </li>
          </ul>
        </nav>
      </div>
    </header>

    <!-- Main Section -->
    <main class="flex-grow-1 d-flex flex-column justify-content-center align-items-center text-center bg-white py-5">
      <h2 class="display-5 fw-bold mb-4">Connect Sponsors with Influencers Seamlessly</h2>
      <p class="lead mb-5 px-3">
        Whether you're a brand looking for the perfect influencer or an influencer seeking sponsorship, 
        SponsorLink makes it easy to connect, collaborate, and grow together.
      </p>
      <div class="d-flex flex-column flex-md-row gap-3">
        <a href="/sponsor/login" class="btn btn-primary btn-lg">Join as Sponsor</a>
        <a href="/influencer/login" class="btn btn-primary btn-lg">Join as Influencer</a>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-primary text-white py-3 mt-auto text-center">
      <p class="mb-0">&copy; 2024 SponsorLink. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: "HomeView",
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
}
</style>