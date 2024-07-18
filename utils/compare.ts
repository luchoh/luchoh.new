function dumpElementAndStyles(element, depth = 0) {
     let output = '';
     const indent = ' '.repeat(depth * 2); // Create an indent based on recursion depth for better readability
   
     // Include element tag and classes or id for better identification
     const tagName = element.tagName.toLowerCase();
     const id = element.id ? ` id="${element.id}"` : '';
     const classes = element.className ? ` class="${element.className}"` : '';
     output += `${indent}<${tagName}${id}${classes}>\n`;  // Simplified display of the element
   
     // Append the computed styles
     output += `${indent}Computed Styles:\n`;
     const styles = window.getComputedStyle(element);
     Array.from(styles).forEach(prop => {
       const value = styles.getPropertyValue(prop);
       output += `${indent}  ${prop}: ${value}\n`;
     });
   
     // Recursively call the function for each child, increasing the depth
     Array.from(element.children).forEach(child => {
       output += dumpElementAndStyles(child, depth + 1);
     });
   
     if (depth === 0) {
       console.log(output); // Print the entire output at once if it's the root call
     } else {
       return output; // Return the output to be added to parent's output
     }
   }