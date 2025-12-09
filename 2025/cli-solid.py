#!/usr/bin/env python3
"""
Complete AoC Setup CLI Application - SOLID Principles Implementation

This is a fully functional CLI application that demonstrates all SOLID principles
in a practical, production-ready implementation.
"""

import argparse
import sys
from datetime import datetime
from typing import Optional

import day_setup_solid as solid_module

def create_application(use_mock: bool = False) -> solid_module.AoCSetupApplication:
    """Factory function to create application with appropriate provider."""
    return solid_module.AoCSetupApplication(use_mock_provider=use_mock)

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Advanced Advent of Code Setup Tool (SOLID Principles)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This tool demonstrates SOLID principles in practice:
  • Single Responsibility: Each class has one clear purpose
  • Open/Closed: Extensible through interfaces and templates
  • Liskov Substitution: Mock providers can substitute real ones
  • Interface Segregation: Small, focused interfaces
  • Dependency Inversion: Depend on abstractions, not concretions

Usage Examples:
  python cli-solid.py --mock                           # Demo with mock data
  python cli-solid.py --day 1 --year 2015             # Historical puzzle
  python cli-solid.py --interactive                    # Guided selection
  python cli-solid.py --demo                           # Show SOLID principles
        """
    )

    # Puzzle selection options (Single Responsibility in CLI parsing)
    selection_group = parser.add_mutually_exclusive_group()
    selection_group.add_argument(
        "--day", type=int, metavar="N",
        help="Day of month (1-25)"
    )
    selection_group.add_argument(
        "--year", type=int, metavar="N",
        help="Year of puzzle"
    )
    selection_group.add_argument(
        "--interactive", action="store_true",
        help="Interactive puzzle selection mode"
    )

    # Configuration options
    parser.add_argument(
        "--folder", type=str,
        help="Custom folder name (auto-generated if not specified)"
    )
    parser.add_argument(
        "--parent-dir", type=str, default="./src",
        help="Parent directory for puzzle folders"
    )

    # Development options (Open/Closed - extensible through flags)
    parser.add_argument(
        "--mock", action="store_true",
        help="Use mock provider (for testing/demonstration)"
    )
    parser.add_argument(
        "--demo", action="store_true",
        help="Demonstrate SOLID principles and exit"
    )

    # Logging options
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Handle demo mode first (Open/Closed - easy to extend)
    if args.demo:
        demonstrate_solid_principles()
        return

    # Validate arguments
    if args.day is not None and not (1 <= args.day <= 25):
        print("❌ Error: Day must be between 1 and 25")
        sys.exit(1)

    if args.year is not None and args.year < 2015:
        print("❌ Error: Year must be 2015 or later (AoC started in 2015)")
        sys.exit(1)

    if (args.day is None) != (args.year is None):
        print("❌ Error: Both --day and --year must be specified together")
        sys.exit(1)

    try:
        # Create application with appropriate provider
        # Dependency Inversion: Application depends on abstraction, not concretion
        app = create_application(use_mock=args.mock)

        print(f"🚀 Advent of Code Setup Tool (SOLID Principles)")
        print(f"📅 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if args.mock:
            print("🎭 Using mock provider (for demonstration)")

        print(f"{'='*60}")

        # Run setup based on selection mode
        if args.interactive or (args.day is None and args.year is None):
            # Interactive mode
            context = app.run()
        else:
            # Manual specification
            folder_name = args.folder or f"day_{args.day:02d}"
            context = app.run(
                day=args.day,
                year=args.year,
                folder_name=folder_name,
                parent_dir=args.parent_dir
            )

        # Display results
        print(f"\\n✅ Setup Complete!")
        print(f"📁 Location: {context.target_directory}")
        print(f"📋 Puzzle: Day {context.day}, {context.year}")

        if context.puzzle_info and "unavailable" not in context.puzzle_info.lower():
            print(f"📄 Title: {context.puzzle_info.split(chr(10))[0]}")

        print(f"\\n🎯 Next Steps:")
        print(f"   1. cd {context.target_directory}")
        print(f"   2. Edit solution.py with your solution")
        print(f"   3. Test with test-input.txt")
        print(f"   4. Run: python solution.py")

        print(f"\\n💡 This setup follows SOLID principles:")
        print(f"   • Single Responsibility: Each component has one job")
        print(f"   • Open/Closed: Easy to extend with new features")
        print(f"   • Liskov Substitution: Mock providers work identically")
        print(f"   • Interface Segregation: Small, focused interfaces")
        print(f"   • Dependency Inversion: Depends on abstractions")

    except KeyboardInterrupt:
        print("\\n❌ Setup interrupted by user")
        sys.exit(1)
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install aocd python-dotenv")
        print("   Or use --mock for demonstration")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
