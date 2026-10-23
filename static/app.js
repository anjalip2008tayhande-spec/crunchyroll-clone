let heroSlides = [];
let trendingAnime = [];
let currentSlideIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
    fetchHomeData();
    setupEventListeners();
});

async function fetchHomeData() {
    const res = await fetch("/api/home");
    const data = await res.json();
    heroSlides = data.hero_slides;
    trendingAnime = data.trending_india;

    renderHeroSlide(currentSlideIndex);
    renderIndicators();
    renderTrendingGrid(trendingAnime);
}

function renderHeroSlide(index) {
    const slide = heroSlides[index];
    if (!slide) return;

    document.getElementById("hero-backdrop").style.backgroundImage = `url('${slide.bg_image}')`;
    document.getElementById("hero-logo").textContent = slide.logo_text;
    document.getElementById("hero-sublogo").textContent = slide.sub_logo;
    document.getElementById("hero-rating").textContent = slide.rating;
    document.getElementById("hero-audio").textContent = slide.audio;
    document.getElementById("hero-genres").textContent = slide.genres.join(", ");
    document.getElementById("hero-desc").textContent = slide.description;
    document.getElementById("hero-btn-text").textContent = slide.episode_btn;

    const bookmarkBtn = document.getElementById("hero-bookmark-btn");
    bookmarkBtn.classList.toggle("active", slide.bookmarked);

    const pills = document.querySelectorAll(".indicator-pill");
    pills.forEach((p, idx) => p.classList.toggle("active", idx === index));
}

function renderIndicators() {
    const container = document.getElementById("carousel-indicators");
    container.innerHTML = "";
    heroSlides.forEach((_, idx) => {
        const pill = document.createElement("div");
        pill.className = `indicator-pill ${idx === currentSlideIndex ? "active" : ""}`;
        pill.addEventListener("click", () => {
            currentSlideIndex = idx;
            renderHeroSlide(currentSlideIndex);
        });
        container.appendChild(pill);
    });
}

function renderTrendingGrid(list) {
    const grid = document.getElementById("trending-grid");
    grid.innerHTML = "";

    list.forEach(item => {
        const card = document.createElement("div");
        card.className = "anime-card";
        card.innerHTML = `
            <div class="poster-wrapper">
                <img src="${item.poster}" alt="${item.title}">
                ${item.bookmarked ? `
                <div class="card-ribbon">
                    <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
                        <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
                    </svg>
                </div>` : ""}
            </div>
            <div class="anime-card-title">${item.title}</div>
            <div class="anime-card-meta">${item.meta}</div>
        `;
        card.addEventListener("click", () => toggleBookmark(item.id));
        grid.appendChild(card);
    });
}

async function toggleBookmark(itemId) {
    await fetch("/api/bookmark", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ item_id: itemId })
    });
    await fetchHomeData();
}

function setupEventListeners() {
    document.getElementById("prev-slide").addEventListener("click", () => {
        currentSlideIndex = (currentSlideIndex - 1 + heroSlides.length) % heroSlides.length;
        renderHeroSlide(currentSlideIndex);
    });

    document.getElementById("next-slide").addEventListener("click", () => {
        currentSlideIndex = (currentSlideIndex + 1) % heroSlides.length;
        renderHeroSlide(currentSlideIndex);
    });

    document.getElementById("hero-bookmark-btn").addEventListener("click", () => {
        const currentSlide = heroSlides[currentSlideIndex];
        if (currentSlide) toggleBookmark(currentSlide.id);
    });

    document.getElementById("close-promo").addEventListener("click", () => {
        document.getElementById("floating-promo").classList.add("hidden");
    });

    // Search Bar Filter
    const searchBtn = document.getElementById("search-btn");
    const searchInput = document.getElementById("search-input");
    searchBtn.addEventListener("click", () => {
        searchInput.classList.toggle("hidden");
        searchInput.focus();
    });

    searchInput.addEventListener("input", (e) => {
        const q = e.target.value.toLowerCase();
        const filtered = trendingAnime.filter(a => a.title.toLowerCase().includes(q));
        renderTrendingGrid(filtered);
    });

    // Watchlist Modal
    const modal = document.getElementById("watchlist-modal");
    document.getElementById("watchlist-nav-btn").addEventListener("click", async () => {
        const res = await fetch("/api/watchlist");
        const data = await res.json();
        const container = document.getElementById("watchlist-items");
        container.innerHTML = data.watchlist.length
            ? data.watchlist.map(a => `<div class="watchlist-row"><span>${a.title}</span><span>Saved 🔖</span></div>`).join("")
            : `<p>No anime bookmarked yet.</p>`;
        modal.classList.remove("hidden");
    });

    document.getElementById("close-modal").addEventListener("click", () => {
        modal.classList.add("hidden");
    });
}