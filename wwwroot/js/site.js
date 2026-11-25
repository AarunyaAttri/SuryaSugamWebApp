(() => {
  const slideshow = document.querySelector("[data-hero-slideshow]");
  if (slideshow) {
    const slides = Array.from(slideshow.querySelectorAll("[data-hero-slide]"));
    const counter = slideshow.querySelector("[data-hero-counter]");
    const previousButton = slideshow.querySelector("[data-hero-previous]");
    const nextButton = slideshow.querySelector("[data-hero-next]");
    const toggleButton = slideshow.querySelector("[data-hero-toggle]");
    const interval = Math.max(Number(slideshow.dataset.interval) || 4000, 1000);
    let activeIndex = Math.max(slides.findIndex((slide) => slide.classList.contains("is-active")), 0);
    let paused = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let rotationTimer;

    const showSlide = (index) => {
      activeIndex = (index + slides.length) % slides.length;
      slides.forEach((slide, slideIndex) => {
        const isActive = slideIndex === activeIndex;
        slide.classList.toggle("is-active", isActive);
        slide.setAttribute("aria-hidden", String(!isActive));
      });
      if (counter) counter.textContent = `${String(activeIndex + 1).padStart(2, "0")} / ${String(slides.length).padStart(2, "0")}`;
    };

    const updateToggleButton = () => {
      const englishLabel = paused ? "Play slideshow" : "Pause slideshow";
      const hindiLabel = paused ? "स्लाइड शो चलाएँ" : "स्लाइड शो रोकें";
      toggleButton.dataset.enAriaLabel = englishLabel;
      toggleButton.dataset.hiAriaLabel = hindiLabel;
      toggleButton.setAttribute("aria-label", document.documentElement.lang === "hi" ? hindiLabel : englishLabel);
      toggleButton.setAttribute("aria-pressed", String(paused));
      toggleButton.textContent = paused ? "▶" : "Ⅱ";
    };

    const setPaused = (shouldPause) => {
      paused = shouldPause;
      window.clearInterval(rotationTimer);
      if (!paused && slides.length > 1) {
        rotationTimer = window.setInterval(() => {
          if (!document.hidden) showSlide(activeIndex + 1);
        }, interval);
      }
      updateToggleButton();
    };

    if (slides.length > 1) {
      previousButton?.addEventListener("click", () => {
        showSlide(activeIndex - 1);
        if (!paused) setPaused(false);
      });
      nextButton?.addEventListener("click", () => {
        showSlide(activeIndex + 1);
        if (!paused) setPaused(false);
      });
      toggleButton?.addEventListener("click", () => setPaused(!paused));
      showSlide(activeIndex);
      setPaused(paused);
    }
  }

  const customOrderForm = document.querySelector("[data-custom-order]");
  const cartCheckoutForm = document.querySelector("[data-cart-checkout]");
  const setSubmissionLanguage = () => {
    const language = document.documentElement.lang === "hi" ? "hi" : "en";
    const customOrderLanguage = customOrderForm?.querySelector("[data-custom-order-language]");
    const cartCheckoutLanguage = cartCheckoutForm?.querySelector("[data-cart-checkout-language]");
    if (customOrderLanguage) customOrderLanguage.value = language;
    if (cartCheckoutLanguage) cartCheckoutLanguage.value = language;
  };

  customOrderForm?.addEventListener("submit", setSubmissionLanguage);
  cartCheckoutForm?.addEventListener("submit", () => {
    setSubmissionLanguage();
    window.setTimeout(() => window.location.reload(), 800);
  });

  const menuToggle = document.querySelector(".menu-toggle");
  const navigation = document.querySelector(".primary-navigation");
  const dropdownToggles = document.querySelectorAll(".nav-dropdown-toggle");

  if (menuToggle && navigation) {
    const closeMenu = () => {
      menuToggle.setAttribute("aria-expanded", "false");
      navigation.classList.remove("is-open");
      dropdownToggles.forEach((toggle) => {
        toggle.setAttribute("aria-expanded", "false");
        toggle.closest(".nav-item-dropdown")?.classList.remove("is-expanded");
      });
    };

    menuToggle.addEventListener("click", () => {
      const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
      menuToggle.setAttribute("aria-expanded", String(!isOpen));
      navigation.classList.toggle("is-open", !isOpen);
    });

    dropdownToggles.forEach((toggle) => {
      toggle.addEventListener("click", () => {
        const item = toggle.closest(".nav-item-dropdown");
        const isExpanded = toggle.getAttribute("aria-expanded") === "true";
        toggle.setAttribute("aria-expanded", String(!isExpanded));
        item?.classList.toggle("is-expanded", !isExpanded);
      });
    });

    navigation.addEventListener("click", (event) => {
      if (event.target.closest("a")) closeMenu();
    });

    document.addEventListener("click", (event) => {
      if (!navigation.contains(event.target) && !menuToggle.contains(event.target)) closeMenu();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && navigation.classList.contains("is-open")) {
        closeMenu();
        menuToggle.focus();
      }
    });

    window.addEventListener("resize", () => {
      if (window.matchMedia("(min-width: 761px)").matches) closeMenu();
    });
  }

  const firstValidationError = document.querySelector(".input-validation-error, .field-validation-error");
  if (firstValidationError) {
    firstValidationError.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  const quantityInput = document.querySelector("[data-quantity-input]");
  if (quantityInput) {
    const clampQuantity = () => {
      const minimum = Number(quantityInput.min) || 1;
      const maximum = Number(quantityInput.max) || 20;
      const quantity = Number.parseInt(quantityInput.value, 10) || minimum;
      quantityInput.value = String(Math.min(maximum, Math.max(minimum, quantity)));
    };

    document.querySelectorAll("[data-quantity-step]").forEach((button) => {
      button.addEventListener("click", () => {
        quantityInput.value = String((Number.parseInt(quantityInput.value, 10) || 1) + Number(button.dataset.quantityStep));
        clampQuantity();
      });
    });

    quantityInput.addEventListener("change", clampQuantity);
  }

  const messageInput = document.querySelector("[data-message-input]");
  const messageCount = document.querySelector("[data-message-count]");
  if (messageInput && messageCount) {
    const updateMessageCount = () => { messageCount.textContent = String(messageInput.value.length); };
    messageInput.addEventListener("input", updateMessageCount);
    updateMessageCount();
  }

  const languageToggle = document.querySelector("[data-language-toggle]");
  const languageStorageKey = "suryasugam-language";

  const updateWhatsAppLinks = (language) => {
    document.querySelectorAll("[data-wa-product]").forEach((link) => {
      const productName = language === "hi" ? link.dataset.productHi : link.dataset.productEn;
      const price = link.dataset.productPrice;
      let message = language === "hi"
        ? `नमस्ते सूर्यसुगम बेकरी, मुझे ${productName} (${price}) का ऑर्डर करना है।`
        : `Hello SuryaSugam Bakery, I would like to order ${productName} (${price}).`;

      if (link.hasAttribute("data-wa-detail")) {
        const form = link.closest("form");
        const read = (name) => form?.querySelector(`[name="Order.${name}"]`)?.value?.trim();
        const translateOrderValue = (value) => language === "hi"
          ? ({ "Pack of 2": "2 का पैक", "Pack of 4": "4 का पैक", "Pack of 8": "8 का पैक", "1 piece": "1 पीस", "Box of 4": "4 का बॉक्स", "Box of 6": "6 का बॉक्स", "200 g": "200 ग्राम", "400 g": "400 ग्राम", "800 g": "800 ग्राम", Regular: "सामान्य", Eggless: "अंडे रहित" }[value] || value)
          : value;
        const size = translateOrderValue(read("Size"));
        const eggOption = translateOrderValue(read("EggOption"));
        const quantity = read("Quantity");
        const city = read("City");
        const area = read("Area");
        const deliveryDate = read("DeliveryDate");
        const timeSlot = read("TimeSlot");
        const details = [
          size && (language === "hi" ? `पैक: ${size}` : `Pack: ${size}`),
          eggOption && (language === "hi" ? `विकल्प: ${eggOption}` : `Option: ${eggOption}`),
          quantity && (language === "hi" ? `मात्रा: ${quantity}` : `Quantity: ${quantity}`),
          area && (language === "hi" ? `इलाका: ${area}` : `Area: ${area}`),
          city && (language === "hi" ? `शहर: ${city}` : `City: ${city}`),
          deliveryDate && (language === "hi" ? `तारीख: ${deliveryDate}` : `Date: ${deliveryDate}`),
          timeSlot && (language === "hi" ? `समय: ${timeSlot}` : `Time: ${timeSlot}`),
          read("Message") && (language === "hi" ? `संदेश: ${read("Message")}` : `Note: ${read("Message")}`)
        ].filter(Boolean);
        if (details.length) message += ` ${details.join(", ")}.`;
      }

      link.href = `https://wa.me/918921986080?text=${encodeURIComponent(message)}`;
      link.setAttribute("aria-label", language === "hi"
        ? `${productName} का व्हाट्सऐप पर ऑर्डर करें`
        : `Order ${productName} on WhatsApp`);
    });

    document.querySelectorAll("[data-wa-cart]").forEach((link) => {
      const message = language === "hi" ? link.dataset.waMessageHi : link.dataset.waMessageEn;
      link.href = `https://wa.me/918921986080?text=${message}`;
    });
  };

  const applyLanguage = (language, savePreference = false) => {
    const selectedLanguage = language === "hi" ? "hi" : "en";
    document.documentElement.lang = selectedLanguage;
    document.documentElement.dataset.language = selectedLanguage;

    const customOrderLanguage = customOrderForm?.querySelector("[data-custom-order-language]");
    const cartCheckoutLanguage = cartCheckoutForm?.querySelector("[data-cart-checkout-language]");
    if (customOrderLanguage) customOrderLanguage.value = selectedLanguage;
    if (cartCheckoutLanguage) cartCheckoutLanguage.value = selectedLanguage;

    document.querySelectorAll("[data-en][data-hi]").forEach((element) => {
      element.textContent = element.dataset[selectedLanguage === "hi" ? "hi" : "en"];
    });

    document.querySelectorAll("[data-en-placeholder][data-hi-placeholder]").forEach((element) => {
      element.placeholder = selectedLanguage === "hi" ? element.dataset.hiPlaceholder : element.dataset.enPlaceholder;
    });

    document.querySelectorAll("[data-en-alt][data-hi-alt]").forEach((element) => {
      element.alt = selectedLanguage === "hi" ? element.dataset.hiAlt : element.dataset.enAlt;
    });

    document.querySelectorAll("[data-en-aria-label][data-hi-aria-label]").forEach((element) => {
      const label = selectedLanguage === "hi" ? element.dataset.hiAriaLabel : element.dataset.enAriaLabel;
      element.setAttribute("aria-label", label);
      if (element.hasAttribute("title")) element.title = label;
    });

    if (languageToggle) {
      languageToggle.setAttribute("aria-pressed", String(selectedLanguage === "hi"));
    }

    updateWhatsAppLinks(selectedLanguage);
    if (savePreference) {
      try { window.localStorage.setItem(languageStorageKey, selectedLanguage); } catch { }
    }
  };

  let savedLanguage = "en";
  try { savedLanguage = window.localStorage.getItem(languageStorageKey) || "en"; } catch { }
  applyLanguage(savedLanguage);

  languageToggle?.addEventListener("click", () => {
    const nextLanguage = document.documentElement.lang === "hi" ? "en" : "hi";
    applyLanguage(nextLanguage, true);
  });

  document.querySelectorAll("[data-wa-detail]").forEach((link) => {
    const form = link.closest("form");
    form?.addEventListener("input", () => updateWhatsAppLinks(document.documentElement.lang));
    form?.addEventListener("change", () => updateWhatsAppLinks(document.documentElement.lang));
  });
})();
