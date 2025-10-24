"""
Command-line interface for Cloud Economizer
"""
import click
from rich.console import Console
from rich.table import Table
import yaml
import os
from pathlib import Path

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Cloud Economizer - Reduce cloud costs with AI-powered optimization"""
    pass


@main.command()
@click.option('--provider', type=click.Choice(['aws', 'azure', 'gcp', 'all']), 
              default='all', help='Cloud provider to analyze')
@click.option('--config', type=click.Path(exists=True), 
              default='config/config.yaml', help='Configuration file path')
@click.option('--profile', help='AWS profile name (for AWS only)')
@click.option('--subscription-id', help='Azure subscription ID (for Azure only)')
@click.option('--project-id', help='GCP project ID (for GCP only)')
def analyze(provider, config, profile, subscription_id, project_id):
    """Analyze cloud infrastructure for cost optimization opportunities"""
    console.print(f"[bold green]🔍 Starting Cloud Economizer Analysis[/bold green]")
    console.print(f"Provider: {provider}")
    
    # Load configuration
    if os.path.exists(config):
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
        console.print(f"✓ Configuration loaded from {config}")
    else:
        console.print(f"[yellow]⚠ Configuration file not found: {config}[/yellow]")
        console.print(f"[yellow]  Using default settings[/yellow]")
        config_data = {}
    
    # Import analysis module
    from cloud_economizer.analysis.analyzer import CloudAnalyzer
    
    # Create analyzer
    analyzer = CloudAnalyzer(config_data)
    
    # Run analysis
    console.print(f"\n[bold]Running analysis...[/bold]")
    try:
        results = analyzer.analyze(
            provider=provider,
            aws_profile=profile,
            azure_subscription_id=subscription_id,
            gcp_project_id=project_id
        )
        
        # Display summary
        display_analysis_summary(results)
        
        console.print(f"\n[bold green]✓ Analysis complete![/bold green]")
        console.print(f"Run 'cloud-economizer report' to generate detailed reports")
        
    except Exception as e:
        console.print(f"[bold red]✗ Analysis failed: {e}[/bold red]")
        raise click.Abort()


@main.command()
@click.option('--format', type=click.Choice(['html', 'pdf', 'json', 'csv']), 
              default='html', help='Report format')
@click.option('--output', type=click.Path(), default='report.html', 
              help='Output file path')
@click.option('--data', type=click.Path(exists=True), 
              default='output/analysis_results.json', help='Analysis data file')
def report(format, output, data):
    """Generate optimization report from analysis results"""
    console.print(f"[bold green]📊 Generating Report[/bold green]")
    console.print(f"Format: {format}")
    console.print(f"Output: {output}")
    
    if not os.path.exists(data):
        console.print(f"[bold red]✗ Analysis data not found: {data}[/bold red]")
        console.print(f"[yellow]Run 'cloud-economizer analyze' first[/yellow]")
        raise click.Abort()
    
    from cloud_economizer.generators.report_generator import ReportGenerator
    
    generator = ReportGenerator()
    generator.generate(data, format, output)
    
    console.print(f"[bold green]✓ Report generated: {output}[/bold green]")


@main.command()
@click.option('--type', type=click.Choice(['terraform', 'shell', 'all']), 
              default='all', help='Type of scripts to generate')
@click.option('--output', type=click.Path(), default='optimizations/', 
              help='Output directory')
@click.option('--data', type=click.Path(exists=True), 
              default='output/analysis_results.json', help='Analysis data file')
def generate(type, output, data):
    """Generate Terraform scripts and automation for optimizations"""
    console.print(f"[bold green]🔧 Generating Optimization Scripts[/bold green]")
    console.print(f"Type: {type}")
    console.print(f"Output: {output}")
    
    if not os.path.exists(data):
        console.print(f"[bold red]✗ Analysis data not found: {data}[/bold red]")
        console.print(f"[yellow]Run 'cloud-economizer analyze' first[/yellow]")
        raise click.Abort()
    
    from cloud_economizer.generators.script_generator import ScriptGenerator
    
    # Create output directory
    Path(output).mkdir(parents=True, exist_ok=True)
    
    generator = ScriptGenerator()
    generated_files = generator.generate(data, type, output)
    
    console.print(f"\n[bold green]✓ Generated {len(generated_files)} files:[/bold green]")
    for file in generated_files:
        console.print(f"  • {file}")


def display_analysis_summary(results):
    """Display a summary table of analysis results"""
    console.print("\n[bold]Analysis Summary:[/bold]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan")
    table.add_column("Findings", justify="right", style="yellow")
    table.add_column("Est. Monthly Savings", justify="right", style="green")
    
    total_savings = 0
    total_findings = 0
    
    for category, data in results.get('categories', {}).items():
        findings_count = data.get('count', 0)
        savings = data.get('savings', 0)
        total_findings += findings_count
        total_savings += savings
        
        table.add_row(
            category,
            str(findings_count),
            f"${savings:,.2f}"
        )
    
    table.add_row(
        "[bold]TOTAL[/bold]",
        f"[bold]{total_findings}[/bold]",
        f"[bold]${total_savings:,.2f}[/bold]"
    )
    
    console.print(table)


if __name__ == '__main__':
    main()
