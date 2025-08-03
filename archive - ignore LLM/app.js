// cerebras.gg - AI Gaming Arcade Application
// Core implementation with Cerebras API integration

class CerebrasGameEngine {
    constructor() {
        this.apiKey = 'csk-m95fkpmkcth8wvwyft9ydhrfe2chth5cr893x2n23dptxf3m';
        this.model = 'qwen-3-coder-480b';
        this.apiUrl = 'https://api.cerebras.ai/v1/chat/completions';
        this.currentGame = null;
        this.agents = {
            generator: { name: 'Game Generator', status: 'Ready', active: false },
            artist: { name: 'ASCII Artist', status: 'Ready', active: false },
            builder: { name: 'Game Builder', status: 'Ready', active: false },
            vibe: { name: 'Vibe Agent', status: 'Ready', active: false }
        };
        this.init();
    }

    init() {
        console.log('🎮 Initializing cerebras.gg AI Gaming Arcade...');
        this.setupEventListeners();
        this.updateStatus('Ready for gaming magic! ✨');
    }

    setupEventListeners() {
        const chatInput = document.getElementById('chatInput');
        const sendBtn = document.getElementById('sendBtn');

        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleUserInput();
            }
        });

        sendBtn.addEventListener('click', () => {
            this.handleUserInput();
        });

        // Auto-focus on input
        chatInput.focus();
    }

    async handleUserInput() {
        const input = document.getElementById('chatInput').value.trim();
        if (!input) return;

        // Clear input and disable button
        document.getElementById('chatInput').value = '';
        document.getElementById('sendBtn').disabled = true;

        // Add user message to chat
        this.addMessage('user', input);

        try {
            // Start game generation process
            await this.generateGame(input);
        } catch (error) {
            console.error('Game generation error:', error);
            this.addMessage('ai', '❌ Oops! My creativity circuits overloaded. Let me try again!');
            this.showError('Game generation failed. Please try again.');
        } finally {
            document.getElementById('sendBtn').disabled = false;
        }
    }

    async generateGame(userRequest) {
        this.showLoading(true);
        this.updateStatus('🤖 Generating your game...');

        try {
            // Step 1: Game Concept Generation
            await this.activateAgent('generator', 'Analyzing your request...');
            const gameResponse = await this.callCerebras(this.buildGameGeneratorPrompt(userRequest));
            const gameData = this.parseGameResponse(gameResponse);

            // Step 2: ASCII Art Generation
            await this.activateAgent('artist', 'Creating ASCII visuals...');
            const artResponse = await this.callCerebras(this.buildArtistPrompt(gameData));
            const artData = this.parseArtResponse(artResponse);

            // Step 3: Game Code Building
            await this.activateAgent('builder', 'Building game mechanics...');
            const codeResponse = await this.callCerebras(this.buildCoderPrompt(gameData, artData));
            const gameCode = this.parseCodeResponse(codeResponse);

            // Step 4: Vibe Check & Polish
            await this.activateAgent('vibe', 'Adding fun factor...');
            const vibeResponse = await this.callCerebras(this.buildVibePrompt(gameData, gameCode));
            const finalGame = this.parseVibeResponse(vibeResponse, gameCode);

            // Deploy the game
            await this.deployGame(finalGame, gameData);

        } catch (error) {
            throw error;
        } finally {
            this.showLoading(false);
            this.resetAgents();
        }
    }

    async callCerebras(prompt) {
        const response = await fetch(this.apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: JSON.stringify({
                model: this.model,
                messages: [{ role: 'user', content: prompt }],
                temperature: 0.8,
                max_tokens: 4096 // Increased token limit for more complex games
            })
        });

        if (!response.ok) {
            const errorBody = await response.text();
            console.error('Cerebras API Error Body:', errorBody);
            throw new Error(`Cerebras API error: ${response.status}`);
        }

        const data = await response.json();
        if (!data.choices || !data.choices[0] || !data.choices[0].message) {
            console.error('Invalid response structure from Cerebras API:', data);
            throw new Error('Invalid response structure from Cerebras API.');
        }
        return data.choices[0].message.content;
    }

    buildGameGeneratorPrompt(userRequest) {
        return `You are the Game Generator Agent for cerebras.gg, the AI gaming arcade.

USER REQUEST: "${userRequest}"

Create a fun game concept based on this request. Return ONLY a JSON object with this structure:
{
    "title": "Game Name",
    "type": "action|puzzle|arcade|simulation",
    "description": "Brief game description",
    "objective": "What the player needs to do",
    "mechanics": ["key gameplay mechanic 1", "mechanic 2", "mechanic 3"],
    "difficulty": "easy|medium|hard",
    "theme": "visual/narrative theme",
    "funFactor": "what makes this game entertaining"
}

Focus on FUN and ENTERTAINMENT. No educational content, just pure gaming joy!`;
    }

    buildArtistPrompt(gameData) {
        return `You are the ASCII Artist Agent. Create ASCII art and visual elements for this game:

GAME: ${JSON.stringify(gameData)}

Generate ASCII art elements. Return ONLY a JSON object:
{
    "playerSprite": "ASCII representation of player character",
    "enemies": ["enemy1 ASCII", "enemy2 ASCII"],
    "objects": ["object1 ASCII", "object2 ASCII"],
    "background": "ASCII background pattern",
    "ui": {
        "border": "ASCII border pattern",
        "score": "Score display format",
        "lives": "Lives display format"
    },
    "animations": {
        "explosion": ["frame1", "frame2", "frame3"],
        "movement": ["frame1", "frame2"]
    }
}

Keep ASCII simple but recognizable. Use single characters for sprites.`;
    }

    buildCoderPrompt(gameData, artData) {
        return `You are the Game Builder Agent. Build executable game logic for:

GAME DATA: ${JSON.stringify(gameData)}
ART DATA: ${JSON.stringify(artData)}

Create a JavaScript game class. Return ONLY valid JavaScript code:

class GeneratedGame {
    constructor(canvas) {
        this.canvas = canvas;
        this.gameState = 'playing';
        this.score = 0;
        this.player = { x: 10, y: 10 };
        // Initialize game state
        this.init();
    }

    init() {
        // Setup game
        this.render();
    }

    update() {
        // Game logic here
        if (this.gameState === 'playing') {
            // Update game state
        }
    }

    render() {
        // Clear and redraw canvas with ASCII art
        this.canvas.innerHTML = '';
        // Render game state
    }

    handleInput(key) {
        // Handle player input
        switch(key) {
            case 'w': case 'ArrowUp': break;
            case 's': case 'ArrowDown': break;
            case 'a': case 'ArrowLeft': break;
            case 'd': case 'ArrowRight': break;
            case ' ': break; // spacebar action
        }
        this.update();
        this.render();
    }

    restart() {
        // Reset game state
        this.init();
    }
}

Make it playable and fun! Include win/lose conditions.`;
    }

    buildVibePrompt(gameData, gameCode) {
        return `You are the Vibe Agent. Review this game and add fun enhancements:

GAME: ${JSON.stringify(gameData)}

Review the game code and suggest fun improvements. Return JSON:
{
    "funEnhancements": ["enhancement 1", "enhancement 2"],
    "encouragement": "Encouraging message for the player",
    "tips": ["gameplay tip 1", "tip 2"],
    "vibeCheck": "overall fun rating out of 10"
}

Focus on making the game more engaging and enjoyable!`;
    }

    parseGameResponse(response) {
        try {
            // Extract JSON from response, even if it's inside backticks
            const jsonMatch = response.match(/```json
([\s\S]*?)
```/) || response.match(/\{[\s\S]*\}/);
            if (jsonMatch) {
                // If we matched the backticks, use the captured group
                const jsonString = jsonMatch[1] || jsonMatch[0];
                return JSON.parse(jsonString);
            }
            throw new Error('No valid JSON found in response');
        } catch (error) {
            console.error('Failed to parse game response:', error);
            // Fallback game
            return {
                title: "ASCII Adventure",
                type: "action",
                description: "A simple ASCII adventure game",
                objective: "Navigate and survive!",
                mechanics: ["movement", "collection", "scoring"],
                difficulty: "medium",
                theme: "retro",
                funFactor: "Classic arcade action!"
            };
        }
    }

    parseArtResponse(response) {
        try {
            const jsonMatch = response.match(/```json
([\s\S]*?)
```/) || response.match(/\{[\s\S]*\}/);
            if (jsonMatch) {
                const jsonString = jsonMatch[1] || jsonMatch[0];
                return JSON.parse(jsonString);
