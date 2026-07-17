(function () {
	// 1. Fetch custom branding from App UI Settings for GamePlan
	fetch(
		'/api/method/frappe.client.get_value?doctype=App UI Setting&filters={"app_name":"gameplan"}&fieldname=["display_name","logo"]'
	)
		.then((r) => r.json())
		.then((res) => {
			const brand = res.message || { display_name: "Nithra Task", logo: "" };
			if (!brand) return;

			// 2. Override Page Title dynamically
			if (brand.display_name) {
				document.title = brand.display_name;
				// Observe title changes to prevent GamePlan's router from resetting it
				const titleObserver = new MutationObserver(() => {
					if (!document.title.includes(brand.display_name)) {
						document.title = brand.display_name;
					}
				});
				const titleNode = document.querySelector("title");
				if (titleNode) {
					titleObserver.observe(titleNode, {
						subtree: true,
						characterData: true,
						childList: true,
					});
				}
			}

			// 3. Dynamically Swap Logo SVGs and dropdown buttons
			const observer = new MutationObserver(() => {
				// A. Replace dropdown menu trigger title "Gameplan"
				const appDropdownSpan = document.querySelector(
					'button[aria-haspopup="menu"] span.text-lg-medium'
				);
				if (appDropdownSpan && appDropdownSpan.textContent === "Gameplan") {
					appDropdownSpan.textContent = brand.display_name;
				}

				// B. Replace GamePlan's SVG logos with the custom logo image
				if (brand.logo) {
					const logoSvgs = document.querySelectorAll("svg.size-7, svg.size-12");
					logoSvgs.forEach((svg) => {
						// Verify it is GamePlan's specific logo SVG (contains path with fill="#F90")
						if (svg.querySelector('path[fill="#F90"]')) {
							const img = document.createElement("img");
							img.src = brand.logo;
							img.className = svg.className.animVal + " object-cover rounded";
							svg.parentNode.replaceChild(img, svg);
						}
					});
				}
			});

			observer.observe(document.body, { childList: true, subtree: true });
		});
})();
