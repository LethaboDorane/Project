import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from django.shortcuts import render
from sklearn.linear_model import LinearRegression
from io import BytesIO
import base64
from .forms import SalesForm
from django.http import HttpResponse

# Function to simulate seasonality effect with an offset for starting month
def add_seasonality(sales, months, amplitude=0.1, period=12, start_month=1):
    seasonal_effect = amplitude * np.sin(2 * np.pi * (np.arange(len(sales) + months) + (start_month - 1)) / period)
    return sales + seasonal_effect[:len(sales)], seasonal_effect[len(sales):]

# Function to add random noise to projections for more realism
def add_random_noise(future_sales, noise_level=0.05):
    noise = np.random.normal(0, noise_level * np.mean(future_sales), len(future_sales))
    return future_sales + noise

# Main view for handling the sales projection
def sales_projection_view(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            sales_data = form.cleaned_data['sales_data']
            expenses_data = form.cleaned_data.get('expenses_data')
            periods = int(form.cleaned_data['months'])

            # Convert sales data to array
            try:
                sales = np.array([float(x) for x in sales_data.split(',') if x.strip()])
            except ValueError:
                return render(request, 'projection_app/sales_projection.html', {
                    'form': form,
                    'error': 'Sales data should contain only numeric values separated by commas.'
                })

            # Convert expenses data to array if provided
            expenses = None
            if expenses_data:
                try:
                    expenses = np.array([float(x) for x in expenses_data.split(',') if x.strip()])
                    if len(expenses) != len(sales):
                        return render(request, 'projection_app/sales_projection.html', {
                            'form': form,
                            'error': 'Expenses data should have the same length as sales data.'
                        })
                except ValueError:
                    return render(request, 'projection_app/sales_projection.html', {
                        'form': form,
                        'error': 'Expenses data should contain only numeric values separated by commas.'
                    })

            # Model fitting and projections (only for sales)
            X = np.arange(1, len(sales) + 1).reshape(-1, 1)
            y = sales.reshape(-1, 1)
            model = LinearRegression()
            model.fit(X, y)

            # Determine trend direction
            slope = model.coef_[0][0]
            if slope > 0:
                trend = "Positive (improving)"
            elif slope < 0:
                trend = "Negative (declining)"
            else:
                trend = "Stagnant"

            # Generate future periods for the projection
            future_X = np.arange(len(sales) + 1, len(sales) + periods + 1).reshape(-1, 1)
            future_sales = model.predict(future_X).flatten()

            # Process seasonality and noise
            sales_with_seasonality, future_seasonal_effect = add_seasonality(sales, periods, period=12)
            future_sales_with_seasonality = future_sales + future_seasonal_effect
            future_sales_noisy = add_random_noise(future_sales_with_seasonality)

            # Generate plot
            fig, ax = plt.subplots()
            graph_type = form.cleaned_data['graph_type']
            create_sales_graph(ax, graph_type, sales_with_seasonality, future_sales_noisy, X, future_X, periods, "Month", expenses)

            # Save plot to a buffer and store it in the session
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_png = buf.getvalue()
            buf.close()

            graph = base64.b64encode(image_png).decode('utf-8')
            request.session['graph_data'] = graph  # Store graph data in session for downloading

            future_sales_list = [(f"Month {i}", f"{sale:.2f}") for i, sale in enumerate(future_sales_noisy, start=len(sales) + 1)]

            return render(request, 'projection_app/sales_projection.html', {
                'form': form,
                'graph': graph,
                'future_sales': future_sales_noisy,
                'future_sales_list': future_sales_list,
                'trend': trend,
            })
        
    else:
        form = SalesForm()

    return render(request, 'projection_app/sales_projection.html', {'form': form})

# Function to handle the graph type and plot creation
def create_sales_graph(ax, graph_type, sales_with_seasonality, future_sales_noisy, X, future_X, periods, period_label, expenses=None):
    # Plot sales
    if graph_type == 'bar':
        ax.bar(range(1, len(X) + 1), sales_with_seasonality, label='Actual Sales (with seasonality)', color='blue')
        ax.bar(range(len(X) + 1, len(X) + periods + 1), future_sales_noisy, label=f'{periods}-{period_label} Projection', color='red')
    elif graph_type == 'line':
        ax.plot(X, sales_with_seasonality, label='Actual Sales (with seasonality)', marker='o')
        ax.plot(future_X, future_sales_noisy, label=f'{periods}-{period_label} Projection', linestyle='--', marker='x', color='red')
    elif graph_type == 'scatter':
        ax.scatter(X, sales_with_seasonality, label='Actual Sales (with seasonality)', color='blue')
        ax.scatter(future_X, future_sales_noisy, label=f'{periods}-{period_label} Projection', color='red')

    # Plot expenses if provided
    if expenses is not None:
        ax.plot(X, expenses, label='Expenses', linestyle=':', marker='s', color='green')

    ax.set(title="Sales Projection", xlabel=period_label, ylabel="Amount")
    ax.legend()

# View to download the generated image
def download_graph(request):
    """Serve the graph as a downloadable image from session data."""
    graph_data = request.session.get('graph_data')
    if graph_data:
        image_data = base64.b64decode(graph_data)  # Decode the base64 image data
        response = HttpResponse(image_data, content_type="image/png")
        response['Content-Disposition'] = 'attachment; filename="sales_projection.png"'
        return response
    else:
        return HttpResponse("No graph available for download.", status=404)
