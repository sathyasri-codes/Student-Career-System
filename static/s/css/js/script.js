document.addEventListener("DOMContentLoaded", function () {

    // =================================
    // 1. MOBILE NAVIGATION MENU
    // =================================

    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.getElementById("navLinks");

    if (menuToggle && navLinks) {

        menuToggle.addEventListener("click", function () {

            navLinks.classList.toggle("show");

            const isOpen = navLinks.classList.contains("show");

            menuToggle.textContent = isOpen ? "✕" : "☰";

            menuToggle.setAttribute("aria-expanded", isOpen);

        });

        navLinks.querySelectorAll("a").forEach(link => {

            link.addEventListener("click", function () {

                navLinks.classList.remove("show");
                menuToggle.textContent = "☰";
                menuToggle.setAttribute("aria-expanded", "false");

            });

        });

        document.addEventListener("click", function (event) {

            if (
                !menuToggle.contains(event.target) &&
                !navLinks.contains(event.target)
            ) {

                navLinks.classList.remove("show");
                menuToggle.textContent = "☰";
                menuToggle.setAttribute("aria-expanded", "false");

            }

        });

    }


    // =================================
    // 2. SEARCH FUNCTION
    // =================================

    function setupSearch(inputId, buttonId, cardSelector) {

        const searchInput = document.getElementById(inputId);
        const searchButton = document.getElementById(buttonId);

        if (!searchInput || !searchButton) return;

        const cards = document.querySelectorAll(cardSelector);

        function searchCards() {

            const searchText = searchInput.value.toLowerCase().trim();

            cards.forEach(card => {

                const cardText = card.textContent.toLowerCase();

                card.style.display =
                    cardText.includes(searchText) ? "" : "none";

            });

        }

        searchButton.addEventListener("click", searchCards);
        searchInput.addEventListener("input", searchCards);

    }


    // =================================
    // 3. GOVERNMENT SCHEMES SEARCH
    // =================================

    setupSearch(
        "schemeSearch",
        "schemeSearchBtn",
        ".scheme-card"
    );


    // =================================
    // 4. ENTRANCE EXAMS SEARCH
    // =================================

    setupSearch(
        "examSearch",
        "examSearchBtn",
        ".exam-card"
    );


    // =================================
    // 5. SCHOLARSHIP SAVE BUTTONS
    // =================================

    const saveButtons = document.querySelectorAll(".save-btn");

    saveButtons.forEach(button => {

        button.addEventListener("click", function () {

            if (this.textContent.trim() === "Save") {

                this.textContent = "Saved";

            } else {

                this.textContent = "Save";

            }

        });

    });


    // =================================
    // 6. SCHOLARSHIP CATEGORY FILTER
    // =================================

    const categoryFilter = document.getElementById("category");
    const levelFilter = document.getElementById("level");

    if (categoryFilter && levelFilter) {

        function filterScholarships() {

            const selectedCategory = categoryFilter.value;
            const selectedLevel = levelFilter.value;

            const scholarshipCards = document.querySelectorAll(
                ".scholarship-card"
            );

            scholarshipCards.forEach(card => {

                const category = card.dataset.category;
                const level = card.dataset.level;

                const categoryMatch =
                    selectedCategory === "all" ||
                    category === selectedCategory;

                const levelMatch =
                    selectedLevel === "all" ||
                    level === "all" ||
                    level === selectedLevel;

                card.style.display =
                    categoryMatch && levelMatch ? "" : "none";

            });

        }

        categoryFilter.addEventListener(
            "change",
            filterScholarships
        );

        levelFilter.addEventListener(
            "change",
            filterScholarships
        );

    }

});