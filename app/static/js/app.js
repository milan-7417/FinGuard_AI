// ===========================================
// FinGuard AI
// Landing Page JavaScript
// ===========================================


// ===========================================
// Smooth Scrolling
// ===========================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        e.preventDefault();

        const target = document.querySelector(
            this.getAttribute("href")
        );

        if (target) {

            target.scrollIntoView({

                behavior: "smooth"

            });

        }

    });

});


// ===========================================
// Navbar Background on Scroll
// ===========================================

const navbar = document.querySelector(".navbar");

window.addEventListener("scroll", () => {

    if (window.scrollY > 50) {

        navbar.style.background = "rgba(15,23,42,0.97)";
        navbar.style.boxShadow = "0 5px 20px rgba(0,0,0,.35)";

    }

    else {

        navbar.style.background = "rgba(15,23,42,.85)";
        navbar.style.boxShadow = "none";

    }

});


// ===========================================
// Fade-in Animation on Scroll
// ===========================================

const observer = new IntersectionObserver(

    (entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("show");

            }

        });

    },

    {

        threshold: 0.15

    }

);

document.querySelectorAll(

    ".card, .feature-card, .about, .workflow, .cta"

).forEach(el => {

    el.classList.add("hidden");

    observer.observe(el);

});


// ===========================================
// Hero Button Animation
// ===========================================

const button = document.querySelector(".btn-primary");

button.addEventListener("mouseenter", () => {

    button.style.transform = "translateY(-5px) scale(1.03)";

});

button.addEventListener("mouseleave", () => {

    button.style.transform = "translateY(0px) scale(1)";

});


// ===========================================
// Hero Image Floating Effect
// ===========================================

const heroImage = document.querySelector(".hero-image img");

let angle = 0;

setInterval(() => {

    angle += 0.02;

    heroImage.style.transform =

        `translateY(${Math.sin(angle) * 10}px)`;

}, 30);

console.log("FinGuard AI Loaded Successfully 🚀");