<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
<style>
.carousel-control-prev-icon {
    background-image: url("data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23000' viewBox='0 0 8 8'%3E%3Cpath d='M5.25 0l-4 4 4 4 1.5-1.5-2.5-2.5 2.5-2.5-1.5-1.5z'/%3E%3C/svg%3E");
}

.carousel-control-next-icon {
    background-image: url("data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23000' viewBox='0 0 8 8'%3E%3Cpath d='M2.75 0l-1.5 1.5 2.5 2.5-2.5 2.5 1.5 1.5 4-4-4-4z'/%3E%3C/svg%3E");
}
</style>
<template>
  <div>
    <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
      <!-- Brand -->
      <a class="navbar-brand" href="#">
        <img src="./Images/moovingLogoBlanco.png" alt= "Logo" style= "width:100px;">
      </a>

      <!-- Links -->
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="#/userlogin">Log in</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#/userregister">Sign up</a>
        </li>
      </ul>
    </nav>
    <!-- Carousel -->
    <b-carousel
      id="carousel-1"
      v-model="slide"
      :interval="4000"
      controls
      indicators
      background="#ababab"
      img-width="1024"
      img-height="480"
      style="text-shadow: 1px 1px 2px #333;"
      @sliding-start="onSlideStart"
      @sliding-end="onSlideEnd"
    >
      <b-carousel-slide text="KEEP ON MOOVING">
        <template #img>
          <img
            class="d-block img-fluid w-100"
            width="1024"
            height="480"
            src="./Images/moto1.jpg"
            alt="image slot"
          >
        </template>
      </b-carousel-slide>
      <!-- Slides with img slot -->
      <!-- Note the classes .d-block and .img-fluid to prevent browser default image alignment -->
      <b-carousel-slide text="LIVE ON THE WHEELS">
        <template #img>
          <img
            class="d-block img-fluid w-100"
            width="1024"
            height="480"
            src="./Images/moto2.jpg"
            alt="image slot"
          >
        </template>
      </b-carousel-slide>
      <b-carousel-slide text="MAKE SMART CHOICES IN YOUR LIFE">
        <template #img>
          <img
            class="d-block img-fluid w-100"
            width="1024"
            height="480"
            src="./Images/moto4.jpg"
            alt="image slot"
          >
        </template>
      </b-carousel-slide>
    </b-carousel>
    <!-- Business Info -->
    <section class= "probootstrap-section probootstrap-cta">
      <div class= "container-sm p-3 my-3 bg-dark text-white">
        <div class= "row">
          <div class="col-sm-8 col-md-offset-2 text-center">
              <p class="h2 sm-2">MOOVING <b-icon icon="building"></b-icon></p>
            </div>
          </div>
        </div>
      </section>
    <b-card-group deck>
      <b-card title="Who are we?" header-border-variant="secondary" align="center">
        <b-card-text>
          A recent business which provides an easy way to drive around the city, chose your favourite type of motorbike and enjoy.
        </b-card-text>
      </b-card>
      <b-card title="How it works?" header-border-variant="secondary" align="center">
        <b-card-text>
          Follow these easy steps:
            <p>1.Create an account.</p>
            <p>2.Login with that account.</p>
            <p>3.We will provide you with a list of motos for you to chose.</p>
            <p>4.Chose the nearest, the most powerful or the one that suits you the best.</p>
            <p>5.Go where it's parked and unlock it.</p>
            <p>6. Enjoy and drive safely!</p>
        </b-card-text>
      </b-card>
      <b-card title="Why us?" header-border-variant="secondary" align="center">
        <b-card-text>
          A lot of options for you only, be eco friendly to our planet and a lot more~
        </b-card-text>
      </b-card>
    </b-card-group>
    <!-- Contact Info -->
    <section class= "probootstrap-section probootstrap-cta">
      <div class= "container-sm p-3 my-3 bg-dark text-white">
        <div class= "row">
          <div class="col-md-8 col-md-offset-2 text-center">
              <h2 class="probootstrap-heading">Contact Us</h2>
              <p class="h4 mb-2">964220611 <b-icon icon="telephone"></b-icon></p>
              <p class="h4 mb-2">mooving@gmail.com <b-icon icon="envelope"></b-icon></p>
            </div>
          </div>
        </div>
      </section>
  </div>
</template>

<script>
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
