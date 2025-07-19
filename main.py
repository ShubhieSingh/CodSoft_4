
"""
Rock-Paper-Scissors Game
A modern GUI-based implementation with score tracking and beautiful interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from enum import Enum
from dataclasses import dataclass
from typing import Optional
import json
import os

class Choice(Enum):
    """Game choices enumeration."""
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

class GameResult(Enum):
    """Game result enumeration."""
    WIN = "win"
    LOSE = "lose"
    TIE = "tie"

@dataclass
class GameStats:
    """Player statistics."""
    wins: int = 0
    losses: int = 0
    ties: int = 0
    total_games: int = 0

    @property
    def win_rate(self) -> float:
        """Calculate win percentage."""
        if self.total_games == 0:
            return 0.0
        return (self.wins / self.total_games) * 100

class RockPaperScissorsGame:
    """Main game class with modern GUI interface."""
    
    # Game rules mapping
    RULES = {
        Choice.ROCK: Choice.SCISSORS,
        Choice.SCISSORS: Choice.PAPER,
        Choice.PAPER: Choice.ROCK
    }
    
    # Choice emojis for visual appeal
    EMOJIS = {
        Choice.ROCK: "🪨",
        Choice.PAPER: "📄",
        Choice.SCISSORS: "✂️"
    }
    
    # Loading animation frames
    LOADING_FRAMES = ["⏳", "⌛", "⏳", "⌛", "⏳", "⌛"]
    THINKING_MESSAGES = [
        "🤔 Computer is thinking...",
        "🔍 Analyzing your choice...",
        "⚡ Calculating the best move...",
        "🎯 Processing decision...",
        "✨ Almost ready...",
        "🎲 Final decision..."
    ]
    
    # Dramatic countdown messages
    COUNTDOWN_MESSAGES = ["3️⃣", "2️⃣", "1️⃣", "🎉"]
    
    # Dark mode color scheme for modern UI
    COLORS = {
        'primary': '#3b82f6',
        'secondary': '#6366f1',
        'success': '#10b981',
        'danger': '#ef4444',
        'warning': '#f59e0b',
        'background': '#0f172a',
        'surface': '#1e293b',
        'card': '#334155',
        'text': '#f1f5f9',
        'text_secondary': '#94a3b8',
        'border': '#475569'
    }

    def __init__(self):
        """Initialize the game."""
        self.stats = GameStats()
        self.load_stats()
        self.animation_running = False
        self.animation_frame = 0
        self.setup_gui()

    def setup_gui(self):
        """Set up the modern GUI interface."""
        # Main window with dark mode
        self.root = tk.Tk()
        self.root.title("Rock Paper Scissors 🎮 - Dark Mode")
        self.root.geometry("800x600")
        self.root.configure(bg=self.COLORS['background'])
        self.root.resizable(False, False)
        
        # Configure styles
        self.setup_styles()
        
        # Create main layout
        self.create_header()
        self.create_game_area()
        self.create_stats_area()
        self.create_footer()
        
        # Center window on screen
        self.center_window()

    def setup_styles(self):
        """Configure ttk styles for modern dark mode appearance."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles for dark mode
        style.configure('Game.TButton',
                       padding=(20, 15),
                       font=('Segoe UI', 12, 'bold'),
                       borderwidth=0,
                       focuscolor='none',
                       background=self.COLORS['primary'],
                       foreground='white')
        
        style.configure('Action.TButton',
                       padding=(15, 10),
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       focuscolor='none',
                       background=self.COLORS['secondary'],
                       foreground='white')
        
        # Configure label styles for dark mode
        style.configure('Title.TLabel',
                       font=('Segoe UI', 24, 'bold'),
                       background=self.COLORS['background'],
                       foreground=self.COLORS['text'])
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 14),
                       background=self.COLORS['background'],
                       foreground=self.COLORS['text_secondary'])
        
        style.configure('Choice.TLabel',
                       font=('Segoe UI', 48),
                       background=self.COLORS['card'],
                       foreground=self.COLORS['text'])
        
        style.configure('Result.TLabel',
                       font=('Segoe UI', 16, 'bold'),
                       background=self.COLORS['card'],
                       foreground=self.COLORS['text'])

    def create_header(self):
        """Create the header section."""
        header_frame = tk.Frame(self.root, bg=self.COLORS['background'], height=100)
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = ttk.Label(header_frame, text="🎮 Rock Paper Scissors", style='Title.TLabel')
        title_label.pack(expand=True)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, 
                                  text="Choose your weapon and challenge the computer!", 
                                  style='Subtitle.TLabel')
        subtitle_label.pack()

    def create_game_area(self):
        """Create the main game area."""
        # Game container
        game_container = tk.Frame(self.root, bg=self.COLORS['background'])
        game_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Choice buttons frame
        buttons_frame = tk.Frame(game_container, bg=self.COLORS['background'])
        buttons_frame.pack(pady=20)
        
        # Create choice buttons
        self.create_choice_buttons(buttons_frame)
        
        # Game result area
        self.create_result_area(game_container)

    def create_choice_buttons(self, parent):
        """Create the choice buttons."""
        ttk.Label(parent, text="Make your choice:", style='Subtitle.TLabel').pack(pady=(0, 15))
        
        button_frame = tk.Frame(parent, bg=self.COLORS['background'])
        button_frame.pack()
        
        # Store button references for enabling/disabling
        self.choice_buttons = []
        
        for choice in Choice:
            btn = tk.Button(button_frame,
                           text=f"{self.EMOJIS[choice]}\n{choice.value.title()}",
                           command=lambda c=choice: self.play_round(c),
                           font=('Segoe UI', 14, 'bold'),
                           bg=self.COLORS['primary'],
                           fg='white',
                           activebackground=self.COLORS['secondary'],
                           activeforeground='white',
                           relief='flat',
                           borderwidth=2,
                           highlightthickness=0,
                           padx=30,
                           pady=20,
                           cursor='hand2')
            btn.pack(side='left', padx=10)
            self.choice_buttons.append(btn)
            
            # Add hover effects for dark mode
            btn.bind("<Enter>", lambda e, b=btn: self._on_button_hover(b) if not self.animation_running else None)
            btn.bind("<Leave>", lambda e, b=btn: self._on_button_leave(b) if not self.animation_running else None)
    
    def _on_button_hover(self, button):
        """Handle button hover effect."""
        if button.cget('state') == 'normal':
            button.configure(bg=self.COLORS['secondary'], 
                           highlightbackground=self.COLORS['text_secondary'])
    
    def _on_button_leave(self, button):
        """Handle button leave effect."""
        if button.cget('state') == 'normal':
            button.configure(bg=self.COLORS['primary'],
                           highlightbackground=self.COLORS['border'])

    def create_result_area(self, parent):
        """Create the result display area."""
        # Result container with modern card design for dark mode
        result_container = tk.Frame(parent, bg=self.COLORS['card'], relief='flat', 
                                   borderwidth=1, highlightbackground=self.COLORS['border'])
        result_container.pack(fill='x', pady=20, ipady=20)
        
        # Battle display
        battle_frame = tk.Frame(result_container, bg=self.COLORS['card'])
        battle_frame.pack(pady=10)
        
        # Player choice display
        player_frame = tk.Frame(battle_frame, bg=self.COLORS['card'])
        player_frame.pack(side='left', padx=40)
        
        ttk.Label(player_frame, text="You", style='Subtitle.TLabel').pack()
        self.player_choice_label = ttk.Label(player_frame, text="❓", style='Choice.TLabel')
        self.player_choice_label.pack()
        
        # VS label
        vs_frame = tk.Frame(battle_frame, bg=self.COLORS['card'])
        vs_frame.pack(side='left', padx=20)
        
        ttk.Label(vs_frame, text="VS", font=('Segoe UI', 20, 'bold'), 
                 background=self.COLORS['card'], foreground=self.COLORS['text_secondary']).pack(pady=40)
        
        # Computer choice display
        computer_frame = tk.Frame(battle_frame, bg=self.COLORS['card'])
        computer_frame.pack(side='left', padx=40)
        
        ttk.Label(computer_frame, text="Computer", style='Subtitle.TLabel').pack()
        self.computer_choice_label = ttk.Label(computer_frame, text="❓", style='Choice.TLabel')
        self.computer_choice_label.pack()
        
        # Result message
        self.result_label = ttk.Label(result_container, text="Choose your weapon to start!", 
                                     style='Result.TLabel')
        self.result_label.pack(pady=10)

    def create_stats_area(self):
        """Create the statistics area."""
        stats_container = tk.Frame(self.root, bg=self.COLORS['surface'], relief='flat', 
                                  borderwidth=1, highlightbackground=self.COLORS['border'])
        stats_container.pack(fill='x', padx=20, pady=10, ipady=15)
        
        ttk.Label(stats_container, text="📊 Game Statistics", 
                 font=('Segoe UI', 14, 'bold'), background=self.COLORS['surface'],
                 foreground=self.COLORS['text']).pack(pady=(0, 10))
        
        stats_frame = tk.Frame(stats_container, bg=self.COLORS['surface'])
        stats_frame.pack()
        
        # Stats display with dark mode colors
        self.wins_label = ttk.Label(stats_frame, text="Wins: 0", 
                                   font=('Segoe UI', 12), background=self.COLORS['surface'],
                                   foreground=self.COLORS['text'])
        self.wins_label.pack(side='left', padx=20)
        
        self.losses_label = ttk.Label(stats_frame, text="Losses: 0", 
                                     font=('Segoe UI', 12), background=self.COLORS['surface'],
                                     foreground=self.COLORS['text'])
        self.losses_label.pack(side='left', padx=20)
        
        self.ties_label = ttk.Label(stats_frame, text="Ties: 0", 
                                   font=('Segoe UI', 12), background=self.COLORS['surface'],
                                   foreground=self.COLORS['text'])
        self.ties_label.pack(side='left', padx=20)
        
        self.winrate_label = ttk.Label(stats_frame, text="Win Rate: 0%", 
                                      font=('Segoe UI', 12), background=self.COLORS['surface'],
                                      foreground=self.COLORS['text'])
        self.winrate_label.pack(side='left', padx=20)

    def create_footer(self):
        """Create the footer with action buttons."""
        footer_frame = tk.Frame(self.root, bg=self.COLORS['background'], height=80)
        footer_frame.pack(fill='x', padx=20, pady=10)
        footer_frame.pack_propagate(False)
        
        button_frame = tk.Frame(footer_frame, bg=self.COLORS['background'])
        button_frame.pack(expand=True)
        
        # Reset stats button with dark mode styling
        reset_btn = tk.Button(button_frame,
                             text="🔄 Reset Stats",
                             command=self.reset_stats,
                             font=('Segoe UI', 10, 'bold'),
                             bg=self.COLORS['warning'],
                             fg='white',
                             activebackground='#d97706',
                             activeforeground='white',
                             relief='flat',
                             borderwidth=1,
                             highlightthickness=0,
                             highlightbackground=self.COLORS['border'],
                             padx=20,
                             pady=10,
                             cursor='hand2')
        reset_btn.pack(side='left', padx=10)
        
        # Add hover effects
        reset_btn.bind("<Enter>", lambda e: reset_btn.configure(bg='#d97706'))
        reset_btn.bind("<Leave>", lambda e: reset_btn.configure(bg=self.COLORS['warning']))
        
        # Exit button with dark mode styling
        exit_btn = tk.Button(button_frame,
                            text="❌ Exit Game",
                            command=self.exit_game,
                            font=('Segoe UI', 10, 'bold'),
                            bg=self.COLORS['danger'],
                            fg='white',
                            activebackground='#dc2626',
                            activeforeground='white',
                            relief='flat',
                            borderwidth=1,
                            highlightthickness=0,
                            highlightbackground=self.COLORS['border'],
                            padx=20,
                            pady=10,
                            cursor='hand2')
        exit_btn.pack(side='right', padx=10)
        
        # Add hover effects
        exit_btn.bind("<Enter>", lambda e: exit_btn.configure(bg='#dc2626'))
        exit_btn.bind("<Leave>", lambda e: exit_btn.configure(bg=self.COLORS['danger']))

    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")

    def disable_choice_buttons(self):
        """Disable choice buttons during animation."""
        # Store reference to choice buttons for easier access
        if hasattr(self, 'choice_buttons'):
            for btn in self.choice_buttons:
                btn.configure(state='disabled', cursor='wait')
    
    def enable_choice_buttons(self):
        """Re-enable choice buttons after animation."""
        if hasattr(self, 'choice_buttons'):
            for btn in self.choice_buttons:
                btn.configure(state='normal', cursor='hand2')
    
    def _disable_buttons_recursive(self, widget):
        """Recursively disable buttons in widget tree."""
        if isinstance(widget, tk.Button) and "choice" in str(widget.cget('command')):
            widget.configure(state='disabled')
        for child in widget.winfo_children():
            self._disable_buttons_recursive(child)
    
    def _enable_buttons_recursive(self, widget):
        """Recursively enable buttons in widget tree."""
        if isinstance(widget, tk.Button) and "choice" in str(widget.cget('command')):
            widget.configure(state='normal')
        for child in widget.winfo_children():
            self._enable_buttons_recursive(child)
    
    def animate_computer_choice(self, player_choice: Choice, computer_choice: Choice):
        """Animate the computer's choice selection with loading effect."""
        total_frames = len(self.LOADING_FRAMES) * 4  # Extended animation
        
        if self.animation_frame < total_frames:
            # Phase 1: Loading animation (first 75% of frames)
            if self.animation_frame < total_frames * 0.75:
                frame_index = self.animation_frame % len(self.LOADING_FRAMES)
                self.computer_choice_label.configure(text=self.LOADING_FRAMES[frame_index])
                
                # Cycle through thinking messages
                message_index = (self.animation_frame // 3) % len(self.THINKING_MESSAGES)
                self.result_label.configure(text=self.THINKING_MESSAGES[message_index])
                
                # Speed up animation as it progresses
                delay = max(80, 200 - (self.animation_frame * 3))
            else:
                # Phase 2: Dramatic countdown (last 25% of frames)
                countdown_phase = self.animation_frame - int(total_frames * 0.75)
                countdown_index = countdown_phase // 3
                
                if countdown_index < len(self.COUNTDOWN_MESSAGES):
                    self.result_label.configure(text=self.COUNTDOWN_MESSAGES[countdown_index])
                    self.computer_choice_label.configure(text="❓")
                    delay = 400  # Slower for dramatic effect
                else:
                    delay = 100
            
            self.animation_frame += 1
            self.root.after(delay, lambda: self.animate_computer_choice(player_choice, computer_choice))
        else:
            # Animation finished, show final result
            self.finish_round(player_choice, computer_choice)
    
    def finish_round(self, player_choice: Choice, computer_choice: Choice):
        """Finish the round by showing final results."""
        # Show computer's final choice with a brief flash effect
        self.computer_choice_label.configure(text="💫")
        self.result_label.configure(text="🎭 Revealing...")
        
        # After a brief pause, show the actual choice
        self.root.after(300, lambda: self._reveal_final_result(player_choice, computer_choice))
    
    def _reveal_final_result(self, player_choice: Choice, computer_choice: Choice):
        """Reveal the final result with dramatic effect."""
        # Show computer's final choice
        self.computer_choice_label.configure(text=self.EMOJIS[computer_choice])
        
        # Determine result
        result = self.determine_winner(player_choice, computer_choice)
        
        # Update stats
        self.update_stats(result)
        
        # Display result with enhanced messages
        self.display_result(player_choice, computer_choice, result)
        
        # Re-enable buttons and reset animation state
        self.animation_running = False
        self.enable_choice_buttons()

    def play_round(self, player_choice: Choice):
        """Play a single round of the game with loading animation."""
        if self.animation_running:
            return  # Prevent multiple animations running simultaneously
        
        # Disable buttons during animation
        self.disable_choice_buttons()
        
        # Show player choice immediately
        self.player_choice_label.configure(text=self.EMOJIS[player_choice])
        
        # Start loading animation for computer choice
        self.animation_running = True
        self.animation_frame = 0
        computer_choice = random.choice(list(Choice))
        
        # Start the loading animation
        self.animate_computer_choice(player_choice, computer_choice)

    def determine_winner(self, player_choice: Choice, computer_choice: Choice) -> GameResult:
        """Determine the winner of the round."""
        if player_choice == computer_choice:
            return GameResult.TIE
        elif self.RULES[player_choice] == computer_choice:
            return GameResult.WIN
        else:
            return GameResult.LOSE

    def update_stats(self, result: GameResult):
        """Update game statistics."""
        self.stats.total_games += 1
        
        if result == GameResult.WIN:
            self.stats.wins += 1
        elif result == GameResult.LOSE:
            self.stats.losses += 1
        else:
            self.stats.ties += 1
        
        self.update_stats_display()
        self.save_stats()

    def update_stats_display(self):
        """Update the statistics display."""
        self.wins_label.configure(text=f"Wins: {self.stats.wins}")
        self.losses_label.configure(text=f"Losses: {self.stats.losses}")
        self.ties_label.configure(text=f"Ties: {self.stats.ties}")
        self.winrate_label.configure(text=f"Win Rate: {self.stats.win_rate:.1f}%")

    def display_result(self, player_choice: Choice, computer_choice: Choice, result: GameResult):
        """Display the round result with enhanced messages."""
        messages = {
            GameResult.WIN: f"🎉 VICTORY! {player_choice.value.title()} beats {computer_choice.value.title()}! 🏆",
            GameResult.LOSE: f"� DEFEAT! {computer_choice.value.title()} beats {player_choice.value.title()}! 😢",
            GameResult.TIE: f"🤝 TIE GAME! You both chose {player_choice.value.title()}! 🎯"
        }
        
        self.result_label.configure(text=messages[result])
        
        # Add a subtle color effect to the result message based on outcome
        if result == GameResult.WIN:
            # Briefly highlight in success color
            self.root.after(100, lambda: self._flash_result_color(self.COLORS['success']))
        elif result == GameResult.LOSE:
            # Briefly highlight in danger color
            self.root.after(100, lambda: self._flash_result_color(self.COLORS['danger']))
        else:
            # Briefly highlight in warning color for tie
            self.root.after(100, lambda: self._flash_result_color(self.COLORS['warning']))
    
    def _flash_result_color(self, color):
        """Flash the result area with a color for visual feedback."""
        # This is a simple implementation - in a more advanced version,
        # we could animate the background color of the result container
        pass

    def reset_stats(self):
        """Reset game statistics."""
        if messagebox.askyesno("Reset Statistics", "Are you sure you want to reset all statistics?"):
            self.stats = GameStats()
            self.update_stats_display()
            self.save_stats()
            
            # Reset visual elements
            self.player_choice_label.configure(text="❓")
            self.computer_choice_label.configure(text="❓")
            self.result_label.configure(text="Statistics reset! Choose your weapon to start!")
            
            # Reset animation state
            self.animation_running = False
            self.animation_frame = 0
            self.enable_choice_buttons()

    def load_stats(self):
        """Load statistics from file."""
        try:
            if os.path.exists('game_stats.json'):
                with open('game_stats.json', 'r') as f:
                    data = json.load(f)
                    self.stats = GameStats(**data)
        except (FileNotFoundError, json.JSONDecodeError):
            self.stats = GameStats()

    def save_stats(self):
        """Save statistics to file."""
        try:
            with open('game_stats.json', 'w') as f:
                json.dump({
                    'wins': self.stats.wins,
                    'losses': self.stats.losses,
                    'ties': self.stats.ties,
                    'total_games': self.stats.total_games
                }, f)
        except Exception as e:
            print(f"Error saving stats: {e}")

    def exit_game(self):
        """Exit the game with confirmation."""
        if messagebox.askyesno("Exit Game", "Are you sure you want to exit?"):
            self.save_stats()
            self.root.quit()

    def run(self):
        """Run the game."""
        # Handle window close button
        self.root.protocol("WM_DELETE_WINDOW", self.exit_game)
        
        # Start the GUI main loop
        self.root.mainloop()

def main():
    """Main function to start the game."""
    print("🎮 Starting Rock-Paper-Scissors Game (Dark Mode)...")
    print("💡 Close the game window or click 'Exit Game' to quit.")
    print("🌙 Enjoy the beautiful dark theme!")
    
    game = RockPaperScissorsGame()
    game.run()

if __name__ == "__main__":
    main()
