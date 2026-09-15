// 3D Drosophila Connectome Brain Visualizer & Action Potential Wave Engine
(function() {
    'use strict';

    let scene, camera, renderer, controls;
    let pointCloud = null;
    let pointsCount = 0;
    let neuropilGroups = {
        sensory_pn: [],
        kenyon_cells: [],
        mbon_output: [],
        dopaminergic: [],
        apl_inhibitory: []
    };

    const COLORS = {
        sensory_pn: [0.0, 0.94, 1.0],      // Cyan #00f0ff
        kenyon_cells: [1.0, 0.84, 0.0],    // Gold #ffd700
        mbon_output: [0.31, 0.98, 0.48],   // Green #50fa7b
        dopaminergic: [1.0, 0.47, 0.78],   // Pink #ff79c6
        apl_inhibitory: [0.74, 0.58, 0.98] // Purple #bd93f9
    };

    let surgeActive = false;
    let surgeStartTime = 0;
    let isInitialized = false;

    window.initBrain3DViewer = function() {
        if (isInitialized) return;
        const container = document.getElementById('brain-3d-canvas-container');
        if (!container || typeof THREE === 'undefined') return;

        const w = container.clientWidth || 1000;
        const h = container.clientHeight || 560;

        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x060911);

        camera = new THREE.PerspectiveCamera(45, w / h, 1, 2500);
        camera.position.set(0, -200, 240);

        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(w, h);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        container.appendChild(renderer.domElement);

        if (typeof THREE.OrbitControls !== 'undefined') {
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.autoRotate = true;
            controls.autoRotateSpeed = 0.9;
        }

        buildBrainPoints();

        document.getElementById('btn-reset-brain-view')?.addEventListener('click', () => {
            camera.position.set(0, -200, 240);
            camera.lookAt(0, 0, 0);
            if (controls) controls.target.set(0, 0, 0);
        });

        document.getElementById('btn-trigger-pulse')?.addEventListener('click', () => {
            surgeActive = true;
            surgeStartTime = performance.now();
        });

        window.addEventListener('resize', () => {
            if (!container || !renderer || !camera) return;
            const nw = container.clientWidth;
            const nh = container.clientHeight;
            camera.aspect = nw / nh;
            camera.updateProjectionMatrix();
            renderer.setSize(nw, nh);
        });

        isInitialized = true;
        animate();
    };

    // Synthesize anatomical point cloud matching Janelia MaleCNS v1.0 geometry
    function buildBrainPoints() {
        const totalPoints = 4800;
        pointsCount = totalPoints;

        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(totalPoints * 3);
        const colors = new Float32Array(totalPoints * 3);

        let ptr = 0;

        // Helper random generator (deterministic seed)
        let s = 12345;
        function rnd() {
            s = (s * 16807) % 2147483647;
            return (s - 1) / 2147483646;
        }
        function rndNorm() {
            let u = 0, v = 0;
            while (u === 0) u = rnd();
            while (v === 0) v = rnd();
            return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
        }

        // 1. Antennal Lobes (Left & Right anterior spheres) - 700 pts
        const n_al = 700;
        for (let i = 0; i < n_al; i++) {
            const side = (i % 2 === 0) ? -1 : 1;
            const cx = side * 45.0, cy = 60.0, cz = -20.0;
            const r = rnd() * 22.0;
            const th = rnd() * Math.PI * 2;
            const ph = rnd() * Math.PI;
            const x = cx + r * Math.sin(ph) * Math.cos(th);
            const y = cy + r * Math.sin(ph) * Math.sin(th);
            const z = cz + r * Math.cos(ph) * 0.85;

            addPoint(ptr, x, y, z, 'sensory_pn', positions, colors);
            ptr++;
        }

        // 2. Mushroom Bodies (Kenyon Cells - Calyx & Vertical/Medial Lobes) - 1800 pts
        const n_mb = 1800;
        for (let i = 0; i < n_mb; i++) {
            const side = (i % 2 === 0) ? -1 : 1;
            let x, y, z;
            if (i % 3 === 0) {
                // Calyx cup
                const cx = side * 75.0, cy = -40.0, cz = 45.0;
                const r = rnd() * 26.0;
                const th = rnd() * Math.PI * 2;
                const ph = rnd() * Math.PI;
                x = cx + r * Math.sin(ph) * Math.cos(th);
                y = cy + r * Math.sin(ph) * Math.sin(th) * 0.8;
                z = cz + r * Math.cos(ph);
            } else if (i % 3 === 1) {
                // Alpha lobe
                const t = rnd();
                x = side * (70.0 * (1 - t) + 25.0 * t + rndNorm() * 4.0);
                y = -35.0 * (1 - t) + 30.0 * t + rndNorm() * 4.0;
                z = 40.0 * (1 - t) + 80.0 * t + rndNorm() * 4.0;
            } else {
                // Beta lobe
                const t = rnd();
                x = side * (25.0 * (1 - t) + 5.0 * t + rndNorm() * 4.0);
                y = 30.0 + rndNorm() * 5.0;
                z = 20.0 * (1 - t) + 35.0 * t + rndNorm() * 4.0;
            }
            addPoint(ptr, x, y, z, 'kenyon_cells', positions, colors);
            ptr++;
        }

        // 3. MBONs (Output Compartments) - 400 pts
        const n_mbon = 400;
        for (let i = 0; i < n_mbon; i++) {
            const side = (i % 2 === 0) ? -1 : 1;
            const cx = side * 30.0, cy = 25.0, cz = 35.0;
            const r = rnd() * 16.0;
            const th = rnd() * Math.PI * 2;
            const ph = rnd() * Math.PI;
            const x = cx + r * Math.sin(ph) * Math.cos(th);
            const y = cy + r * Math.sin(ph) * Math.sin(th);
            const z = cz + r * Math.cos(ph);
            addPoint(ptr, x, y, z, 'mbon_output', positions, colors);
            ptr++;
        }

        // 4. Central Complex / Dopaminergic DANs - 600 pts
        const n_cx = 600;
        for (let i = 0; i < n_cx; i++) {
            const r = 10.0 + rnd() * 18.0;
            const th = rnd() * Math.PI * 2;
            const x = r * Math.cos(th);
            const y = 5.0 + rndNorm() * 8.0;
            const z = 15.0 + r * Math.sin(th) * 0.5;
            addPoint(ptr, x, y, z, 'dopaminergic', positions, colors);
            ptr++;
        }

        // 5. Optic Lobes & Lateral Neuropils - 1000 pts
        const n_ol = 1000;
        for (let i = 0; i < n_ol; i++) {
            const side = (i % 2 === 0) ? -1 : 1;
            const cx = side * 135.0;
            const cy = -30.0 + rnd() * 70.0;
            const cz = -10.0 + rnd() * 70.0;
            const x = cx + rndNorm() * 18.0 * side;
            const y = cy + rndNorm() * 14.0;
            const z = cz + rndNorm() * 16.0;
            addPoint(ptr, x, y, z, 'apl_inhibitory', positions, colors);
            ptr++;
        }

        // 6. Remaining Descending Pathways
        while (ptr < totalPoints) {
            const t = rnd();
            const x = rndNorm() * 12.0 * (1 - t * 0.5);
            const y = -20.0 - t * 80.0 + rndNorm() * 7.0;
            const z = -15.0 - t * 40.0 + rndNorm() * 7.0;
            addPoint(ptr, x, y, z, 'sensory_pn', positions, colors);
            ptr++;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 3.2,
            vertexColors: true,
            transparent: true,
            opacity: 0.90,
            blending: THREE.AdditiveBlending
        });

        pointCloud = new THREE.Points(geometry, material);
        scene.add(pointCloud);
    }

    function addPoint(idx, x, y, z, neuropil, positions, colors) {
        positions[idx * 3]     = x;
        positions[idx * 3 + 1] = y;
        positions[idx * 3 + 2] = z;

        neuropilGroups[neuropil].push(idx);

        const c = COLORS[neuropil];
        colors[idx * 3]     = c[0];
        colors[idx * 3 + 1] = c[1];
        colors[idx * 3 + 2] = c[2];
    }

    // Animation loop: biological firing pulse waves & olfactory surges
    function animate() {
        requestAnimationFrame(animate);

        if (controls) controls.update();

        if (pointCloud) {
            const colorsAttr = pointCloud.geometry.attributes.color;
            const now = performance.now();
            const t = now * 0.003;

            // Check if surge trigger active (propagates from Antennal Lobe -> KC -> MBON)
            let surgeAge = surgeActive ? (now - surgeStartTime) / 1000.0 : 999.0;
            if (surgeAge > 4.0) surgeActive = false;

            for (const neuropil in neuropilGroups) {
                const base = COLORS[neuropil];
                const list = neuropilGroups[neuropil];

                // Base biological oscillations per neuropil
                let freq = 1.0;
                let surgeBoost = 0.0;

                if (neuropil === 'sensory_pn') {
                    freq = 2.4;
                    if (surgeAge < 1.2) surgeBoost = Math.max(0, 1.0 - surgeAge / 1.2) * 2.2;
                } else if (neuropil === 'kenyon_cells') {
                    freq = 1.2;
                    if (surgeAge >= 0.4 && surgeAge < 2.2) surgeBoost = Math.max(0, 1.0 - Math.abs(surgeAge - 1.2) / 1.0) * 2.8;
                } else if (neuropil === 'mbon_output') {
                    freq = 3.1;
                    if (surgeAge >= 1.0 && surgeAge < 3.0) surgeBoost = Math.max(0, 1.0 - Math.abs(surgeAge - 1.8) / 1.0) * 3.5;
                } else if (neuropil === 'dopaminergic') {
                    freq = 0.8;
                    if (surgeAge >= 1.5 && surgeAge < 3.5) surgeBoost = Math.max(0, 1.0 - Math.abs(surgeAge - 2.4) / 1.0) * 3.0;
                } else if (neuropil === 'apl_inhibitory') {
                    freq = 1.6;
                }

                for (let i = 0; i < list.length; i++) {
                    const idx = list[i];
                    // Natural asynchronous phase shift per neuron
                    const phase = (idx % 37) * 0.17;
                    const pulse = 0.75 + Math.sin(t * freq + phase) * 0.40 + surgeBoost;

                    colorsAttr.array[idx * 3]     = Math.min(1.0, base[0] * pulse);
                    colorsAttr.array[idx * 3 + 1] = Math.min(1.0, base[1] * pulse);
                    colorsAttr.array[idx * 3 + 2] = Math.min(1.0, base[2] * pulse);
                }
            }

            colorsAttr.needsUpdate = true;
        }

        if (renderer && scene && camera) {
            renderer.render(scene, camera);
        }
    }
})();
