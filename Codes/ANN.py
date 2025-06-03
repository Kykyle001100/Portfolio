import numpy as np
import json
import time

# Activation function and its derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# Define the neural network class
class ANN:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.1, isdebugging=False):
        self.hidden_weights = np.array([
            [
            0.10907717566917696,
            -0.25500651702828375,
            0.7326207957626404,
            0.7444148620256303
        ],
        [
            1.1597333120966602,
            -0.34867113043519016,
            1.8849647498084718,
            -1.4890390184688675
        ],
        [
            -0.17877903821787489,
            0.5213866750318044,
            0.05292237006816118,
            0.4069295708004492
        ],
        [
            -0.4707410283185963,
            0.5118862546949303,
            -1.626499631704774,
            0.22353062606733565
        ],
        [
            -1.7682517480629636,
            -0.043600471419713634,
            -1.2336080022638634,
            1.4598360259996224
        ],
        [
            -0.29533185445794,
            -1.621508968767382,
            -0.5380620961867573,
            0.9440576401313474
        ],
        [
            -0.38613162911097915,
            0.8322015465142631,
            0.9792880217238908,
            -0.6436551421398867
        ],
        [
            0.4751402150312967,
            0.7948479108008784,
            -0.09336618151323249,
            0.23021776782160705
        ]
        ])
        self.output_weights = np.array([
        [
            0.20507381024942728,
            0.2652460077186108,
            -0.09781397325354338,
            -0.1537285867482554,
            -0.9334935588188555,
            -0.7823351201375983
        ],
        [
            1.1943562032378383,
            -1.632054544832257,
            0.8666595010556951,
            -0.02357886207034342,
            -0.8223291328944131,
            -1.9675468663327251
        ],
        [
            1.8075883021345214,
            2.1461343755835594,
            0.16313477546708452,
            -0.23028847923223783,
            -1.9531020629986608,
            -0.4760114269653556
        ],
        [
            0.712788562296105,
            -0.10193991207391793,
            -1.1696165633778404,
            1.844520307545567,
            0.9801731826299748,
            0.7160753957024779
        ]
        ])
        self.learning_rate = learning_rate

        self.debug = isdebugging

    def forward(self, X):
        self.hidden_layer = sigmoid(np.dot(X, self.hidden_weights))
        self.output_layer = sigmoid(np.dot(self.hidden_layer, self.output_weights))
        return self.output_layer

    def backward(self, X, y):
        output_error = y - self.output_layer
        output_delta = output_error * sigmoid_derivative(self.output_layer)

        hidden_error = np.dot(output_delta, self.output_weights.T)
        hidden_delta = hidden_error * sigmoid_derivative(self.hidden_layer)

        # Update weights
        self.output_weights += self.learning_rate * np.dot(self.hidden_layer.T, output_delta)
        self.hidden_weights += self.learning_rate * np.dot(X.T, hidden_delta)
        
        # Compute loss (Mean Squared Error)
        loss = np.mean(output_error ** 2)
        return loss

    def train(self, X, y, epochs=1000):
        for i in range(epochs):
            self.forward(X)
            loss = self.backward(X, y)
            if i % 1000 == 0 and self.debug:
                time.sleep(0.0001)
                print(f"Epoch {i}: Loss = {loss:.4f}")

    def predict(self, X):
        return self.forward(X).round()
    
    def __str__(self):
        return json.dumps({
            "hidden_weights": self.hidden_weights.tolist(),
            "output_weights": self.output_weights.tolist(),
            "learning_rate": self.learning_rate
        }, indent=4)

# Example usage
if __name__ == "__main__":
    # Input (no weights applied to this layer, directly passed to hidden layer)
    X = np.array([
        [1, 0, 0, 1, 1, 0, 0, 1], # Sugar + Sugar
        [1, 1, 0, 0, 1, 0, 0, 1], # Organic Acid + Sugar
        [1, 1, 0, 0, 0, 0, 1, 1], # Organic Acid + Phosphoric Acid
        [1, 0, 0, 1, 0, 0, 1, 1], # Sugar + Phosphoric Acid
        [1, 1, 0, 0, 1, 1, 0, 0], # Organic Acid + Organic Acid
    ])
    
    # Output labels
    y = np.array([
        [1, 0, 0, 1, 1, 0], # Polysaccharide
        [1, 1, 0, 1, 0, 0], # Acidic Sugar
        [1, 1, 1, 0, 0, 0], # Organic Acid Phosphate
        [1, 0, 1, 1, 0, 0], # Sugar Phosphate
        [1, 1, 0, 1, 0, 1], # Organic Acid Isomer
    ])
    
    # Initialize and train the network
    ann = ANN(input_size=8, hidden_size=4, output_size=6, learning_rate=0.0000124, isdebugging=True)
    #ann.train(X, y, epochs=1000000)
    
    # Predictions
    predictions = ann.predict(X)
    print("Predictions after training:")
    print(predictions)
    
    # Print the ANN structure as JSON
    print(str(ann))
