#!/usr/bin/env python3
"""
Advent of Code Setup - SOLID Principles Refactoring

Refactored to follow SOLID principles:
- Single Responsibility: Each class has one reason to change
- Open/Closed: Open for extension, closed for modification
- Liskov Substitution: Derived classes can substitute base classes
- Interface Segregation: Small, focused interfaces
- Dependency Inversion: Depend on abstractions, not concretions
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
import os

# ==================== SOLID PRINCIPLE: INTERFACE SEGREGATION ====================

class AoCProviderInterface(ABC):
    """Interface for AoC data providers - following Interface Segregation"""

    @abstractmethod
    def get_input_data(self, day: int, year: int) -> str:
        """Get raw input data for a puzzle."""
        pass

    @abstractmethod
    def get_puzzle_info(self, day: int, year: int) -> str:
        """Get puzzle description and information."""
        pass

class FileManagerInterface(ABC):
    """Interface for file operations - following Interface Segregation"""

    @abstractmethod
    def create_directory(self, path: Path) -> Path:
        """Create directory structure."""
        pass

    @abstractmethod
    def write_file(self, path: Path, content: str) -> Path:
        """Write content to file."""
        pass

class DateValidatorInterface(ABC):
    """Interface for date validation - following Interface Segregation"""

    @abstractmethod
    def validate_date(self, day: int, year: int) -> 'ValidationResult':
        """Validate if date is valid for AoC."""
        pass

class PuzzleSelectorInterface(ABC):
    """Interface for puzzle selection logic - following Interface Segregation"""

    @abstractmethod
    def suggest_puzzle(self) -> 'PuzzleSuggestion':
        """Suggest appropriate puzzle based on current context."""
        pass

# ==================== SOLID PRINCIPLE: SINGLE RESPONSIBILITY ====================

@dataclass(frozen=True)
class ValidationResult:
    """Value object for validation results - follows Single Responsibility"""
    is_valid: bool
    status: str
    message: str

@dataclass(frozen=True)
class PuzzleSuggestion:
    """Value object for puzzle suggestions - follows Single Responsibility"""
    day: int
    year: int
    reason: str

@dataclass
class PuzzleContext:
    """Context object containing all puzzle setup information"""
    day: int
    year: int
    input_data: str
    puzzle_info: str
    folder_name: str
    parent_directory: Path
    target_directory: Path

class DateValidator(DateValidatorInterface):
    """Date validation logic - Single Responsibility: only validates dates"""

    def __init__(self, current_year: int = None):
        self.current_year = current_year or datetime.now().year

    def validate_date(self, day: int, year: int) -> ValidationResult:
        """Validate AoC date according to business rules."""
        # Basic range validation
        if not (1 <= day <= 25):
            return ValidationResult(
                False,
                "Invalid day",
                f"Day must be between 1 and 25, got {day}"
            )

        if year < 2015:
            return ValidationResult(
                False,
                "Invalid year",
                f"Year must be 2015 or later (AoC started in 2015), got {year}"
            )

        if year > self.current_year + 1:
            return ValidationResult(
                False,
                "Invalid year",
                f"Year too far in future: {year} (current: {self.current_year})"
            )

        # Temporal validation
        puzzle_date = date(year, 12, day)
        today = date.today()

        if puzzle_date > today:
            days_ahead = (puzzle_date - today).days
            return ValidationResult(
                False,
                "Future puzzle",
                f"Puzzle releases in {days_ahead} day{'s' if days_ahead != 1 else ''}"
            )

        # Current year validation
        if year == self.current_year:
            current_month = datetime.now().month
            current_day = datetime.now().day

            if current_month == 12:
                if day > current_day:
                    days_until = day - current_day
                    return ValidationResult(
                        False,
                        "Not released",
                        f"Releases in {days_until} day{'s' if days_until != 1 else ''}"
                    )
            elif current_month > 12:
                # Past December - year is complete
                pass

        return ValidationResult(
            True,
            "Available",
            self._get_status_message(year, day)
        )

    def _get_status_message(self, year: int, day: int) -> str:
        """Get descriptive status message."""
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day

        if year == current_year:
            if current_month == 12:
                if day == current_day:
                    return "Current AoC day"
                elif day < current_day:
                    return "Historical day this year"
                else:
                    return "Future AoC day"
            elif current_month > 12:
                return "Completed AoC year"
            else:
                return "Historical data for current year"

        return "Historical AoC puzzle"

class PuzzleSelector(PuzzleSelectorInterface):
    """Puzzle selection logic - Single Responsibility: only selects puzzles"""

    def __init__(self, date_validator: DateValidator):
        self.date_validator = date_validator

    def suggest_puzzle(self) -> PuzzleSuggestion:
        """Suggest best puzzle based on current season and context."""
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day

        # Check if it's AoC season
        if current_month == 12 and 1 <= current_day <= 25:
            return PuzzleSuggestion(
                current_day,
                current_year,
                f"Today is Day {current_day} of AoC {current_year}!"
            )

        # Past December 25th
        if current_month == 12 and current_day > 25:
            return PuzzleSuggestion(
                1,
                current_year,
                f"AoC {current_year} has ended, suggesting Day 1"
            )

        # Default to classic first puzzle
        return PuzzleSuggestion(
            1,
            2015,
            "Outside AoC season, suggesting the classic first puzzle"
        )

    def get_available_years(self) -> List[int]:
        """Get list of years with available puzzles."""
        current_year = datetime.now().year
        return list(range(2015, current_year + 1))

# ==================== SOLID PRINCIPLE: DEPENDENCY INVERSION ====================

class RealAoCProvider(AoCProviderInterface):
    """Real AoC provider - depends on abstraction, not concretion"""

    def __init__(self):
        try:
            from aocd import get_data, get_puzzle
            self._get_data = get_data
            self._get_puzzle = get_puzzle
        except ImportError:
            raise ImportError("aocd package required. Install with: pip install aocd")

    def get_input_data(self, day: int, year: int) -> str:
        """Get input data from AoC API."""
        return self._get_data(day=day, year=year, block=False)

    def get_puzzle_info(self, day: int, year: int) -> str:
        """Get puzzle information from AoC API."""
        return str(self._get_puzzle(day=day, year=year))

class MockAoCProvider(AoCProviderInterface):
    """Mock provider for testing - follows Dependency Inversion"""

    def get_input_data(self, day: int, year: int) -> str:
        return f"Mock input data for day {day}, year {year}"

    def get_puzzle_info(self, day: int, year: int) -> str:
        return f"Day {day} Title - Mock puzzle for year {year}"

class FileManager(FileManagerInterface):
    """File management operations - Single Responsibility: only file operations"""

    def create_directory(self, path: Path) -> Path:
        """Create directory structure."""
        path.mkdir(parents=True, exist_ok=True)
        return path

    def write_file(self, path: Path, content: str) -> Path:
        """Write content to file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return path

    def make_executable(self, path: Path) -> None:
        """Make file executable on Unix systems."""
        if os.name != 'nt':
            try:
                path.chmod(0o755)
            except Exception as e:
                logging.warning(f"Could not make {path} executable: {e}")

# ==================== SOLID PRINCIPLE: OPEN/CLOSED ====================

class FileTemplate(ABC):
    """Abstract template for file creation - Open for extension, closed for modification"""

    @abstractmethod
    def get_filename(self) -> str:
        """Get the filename for this template."""
        pass

    @abstractmethod
    def generate_content(self, context: PuzzleContext) -> str:
        """Generate file content based on context."""
        pass

class InputFileTemplate(FileTemplate):
    """Template for input file - extends FileTemplate"""

    def get_filename(self) -> str:
        return "input.txt"

    def generate_content(self, context: PuzzleContext) -> str:
        return context.input_data

class TestInputFileTemplate(FileTemplate):
    """Template for test input file"""

    def get_filename(self) -> str:
        return "test-input.txt"

    def generate_content(self, context: PuzzleContext) -> str:
        return f"# Test input for Day {context.day}, {context.year}\n# Add your test cases here\n"

class SolutionFileTemplate(FileTemplate):
    """Template for solution file"""

    def get_filename(self) -> str:
        return "solution.py"

    def generate_content(self, context: PuzzleContext) -> str:
        template = '''#!/usr/bin/env python3
"""
Advent of Code Day {day}, {year}

Puzzle: {puzzle_title}
"""

def solve_part_1(data: str) -> int:
    """Solve part 1 of the puzzle."""
    # TODO: Implement solution
    lines = data.strip().split('\\n')
    # Your solution here
    return 0

def solve_part_2(data: str) -> int:
    """Solve part 2 of the puzzle."""
    # TODO: Implement solution
    lines = data.strip().split('\\n')
    # Your solution here
    return 0

def main():
    """Main execution function."""
    with open("input.txt", "r") as f:
        data = f.read().strip()

    result_1 = solve_part_1(data)
    result_2 = solve_part_2(data)

    print(f"Part 1: {{result_1}}")
    print(f"Part 2: {{result_2}}")

if __name__ == "__main__":
    main()
'''
        return template.format(
            day=context.day,
            year=context.year,
            puzzle_title=context.puzzle_info.split('\\n')[0] if context.puzzle_info else f"Day {context.day}"
        )

# ==================== Liskov Substitution Principle Demonstration ====================

class BaseFileCreator(ABC):
    """Base class for file creators - supports Liskov Substitution"""

    def __init__(self, templates: List[FileTemplate], file_manager: FileManager):
        self.templates = templates
        self.file_manager = file_manager

    @abstractmethod
    def create_files(self, context: PuzzleContext) -> List[Path]:
        """Create files based on templates and context."""
        pass

class StandardFileCreator(BaseFileCreator):
    """Standard file creator - can substitute for BaseFileCreator"""

    def create_files(self, context: PuzzleContext) -> List[Path]:
        """Create standard AoC files."""
        created_files = []

        for template in self.templates:
            file_path = context.target_directory / template.get_filename()
            content = template.generate_content(context)

            self.file_manager.write_file(file_path, content)
            created_files.append(file_path)

            # Make solution file executable
            if template.get_filename() == "solution.py":
                self.file_manager.make_executable(file_path)

        return created_files

# ==================== SOLID PRINCIPLE: SINGLE RESPONSIBILITY ====================

class AoCSetupOrchestrator:
    """Orchestrates the entire setup process - Single Responsibility: coordinates setup"""

    def __init__(
        self,
        aoc_provider: AoCProviderInterface,
        date_validator: DateValidatorInterface,
        puzzle_selector: PuzzleSelectorInterface,
        file_creator: BaseFileCreator,
        logger: logging.Logger = None
    ):
        self.aoc_provider = aoc_provider
        self.date_validator = date_validator
        self.puzzle_selector = puzzle_selector
        self.file_creator = file_creator
        self.logger = logger or logging.getLogger(__name__)

    def setup_puzzle(
        self,
        day: int,
        year: int,
        folder_name: str,
        parent_directory: str
    ) -> PuzzleContext:
        """Complete puzzle setup orchestration."""
        self.logger.info(f"Starting setup for Day {day}, {year}")

        # Validate date
        validation_result = self.date_validator.validate_date(day, year)
        if not validation_result.is_valid:
            raise ValueError(f"Invalid date: {validation_result.message}")

        # Fetch puzzle data
        try:
            input_data = self.aoc_provider.get_input_data(day, year)
            puzzle_info = self.aoc_provider.get_puzzle_info(day, year)
        except Exception as e:
            self.logger.warning(f"Failed to fetch puzzle data: {e}")
            input_data = f"# Puzzle data unavailable for Day {day}, {year}\\n"
            puzzle_info = f"Day {day}, {year} (Data unavailable)"

        # Create context
        parent_path = Path(parent_directory)
        target_path = parent_path / folder_name

        context = PuzzleContext(
            day=day,
            year=year,
            input_data=input_data,
            puzzle_info=puzzle_info,
            folder_name=folder_name,
            parent_directory=parent_path,
            target_directory=target_path
        )

        # Create files
        created_files = self.file_creator.create_files(context)

        self.logger.info(f"Setup complete. Created {len(created_files)} files")

        return context

class InteractivePuzzleChooser:
    """Interactive puzzle selection - Single Responsibility: handles user interaction"""

    def __init__(self, puzzle_selector: PuzzleSelectorInterface):
        self.puzzle_selector = puzzle_selector

    def choose_puzzle_interactively(self) -> PuzzleSuggestion:
        """Allow user to choose puzzle interactively."""
        print("\\n🎯 No specific puzzle requested. Let me suggest some options:")

        # Show suggestion
        suggestion = self.puzzle_selector.suggest_puzzle()
        print(f"\\n💡 RECOMMENDED: Day {suggestion.day}, {suggestion.year}")
        print(f"   Reason: {suggestion.reason}")

        # Show available years
        available_years = self.puzzle_selector.get_available_years()
        print(f"\\n📚 Available years: {min(available_years)}-{max(available_years)}")

        # Interactive selection loop
        while True:
            try:
                print(f"\\nOptions:")
                print(f"1. Use recommendation (Day {suggestion.day}, {suggestion.year})")
                print(f"2. Choose specific day/year")
                print(f"3. Exit")

                choice = input("Select option (1-3): ").strip()

                if choice == "1":
                    return suggestion
                elif choice == "2":
                    day = int(input("Day (1-25): "))
                    year = int(input("Year: "))
                    return PuzzleSuggestion(day, year, "Manual selection")
                elif choice == "3":
                    print("Goodbye! 👋")
                    sys.exit(0)
                else:
                    print("Invalid choice. Please try again.")

            except (ValueError, KeyboardInterrupt):
                print("\\nGoodbye! 👋")
                sys.exit(0)

# ==================== MAIN APPLICATION (Following SOLID) ====================

class AoCSetupApplication:
    """Main application class - coordinates all components"""

    def __init__(self, use_mock_provider: bool = False):
        # Dependencies injected through constructor
        self.logger = logging.getLogger(__name__)
        self.date_validator = DateValidator()
        self.puzzle_selector = PuzzleSelector(self.date_validator)

        if use_mock_provider:
            self.aoc_provider = MockAoCProvider()
        else:
            self.aoc_provider = RealAoCProvider()

        file_manager = FileManager()
        templates = [
            InputFileTemplate(),
            TestInputFileTemplate(),
            SolutionFileTemplate()
        ]
        self.file_creator = StandardFileCreator(templates, file_manager)

        self.orchestrator = AoCSetupOrchestrator(
            self.aoc_provider,
            self.date_validator,
            self.puzzle_selector,
            self.file_creator,
            self.logger
        )

        self.chooser = InteractivePuzzleChooser(self.puzzle_selector)

    def run(self, day: Optional[int] = None, year: Optional[int] = None,
           folder_name: Optional[str] = None, parent_dir: str = "./src") -> PuzzleContext:
        """Run the complete setup process."""
        # Determine puzzle selection strategy
        if day is not None and year is not None:
            # Manual specification
            suggestion = PuzzleSuggestion(day, year, "Manual specification")
        else:
            # Interactive selection
            suggestion = self.chooser.choose_puzzle_interactively()

        # Generate folder name if not provided
        if folder_name is None:
            folder_name = f"day_{suggestion.day:02d}"

        # Setup the puzzle
        return self.orchestrator.setup_puzzle(
            suggestion.day,
            suggestion.year,
            folder_name,
            parent_dir
        )

# ==================== DEMONSTRATION ====================

def demonstrate_solid_principles():
    """Demonstrate how the refactored code follows SOLID principles."""
    print("🏗️  SOLID Principles Demonstration")
    print("=" * 60)

    # Single Responsibility: Each class has one job
    print("\\n📋 Single Responsibility Principle:")
    print("   • DateValidator: Only validates dates")
    print("   • PuzzleSelector: Only selects puzzles")
    print("   • FileManager: Only manages files")
    print("   • AoCProvider: Only fetches AoC data")

    # Open/Closed: Extensible through templates
    print("\\n🔓 Open/Closed Principle:")
    print("   • FileTemplate: Can be extended with new templates")
    print("   • BaseFileCreator: Can be extended with new creators")
    print("   • AoCProvider: Can be extended with new providers")

    # Liskov Substitution: Substitutable implementations
    print("\\n🔄 Liskov Substitution Principle:")
    print("   • MockAoCProvider can substitute RealAoCProvider")
    print("   • StandardFileCreator can substitute BaseFileCreator")

    # Interface Segregation: Small, focused interfaces
    print("\\n🎯 Interface Segregation Principle:")
    print("   • AoCProviderInterface: Only AoC-related methods")
    print("   • FileManagerInterface: Only file-related methods")
    print("   • DateValidatorInterface: Only validation methods")

    # Dependency Inversion: Depend on abstractions
    print("\\n⬇️  Dependency Inversion Principle:")
    print("   • AoCSetupOrchestrator depends on AoCProviderInterface")
    print("   • StandardFileCreator depends on FileManagerInterface")
    print("   • AoCSetupApplication depends on abstractions, not concretions")

    print("\\n✅ Result: Highly testable, maintainable, and extensible code!")

if __name__ == "__main__":
    demonstrate_solid_principles()
