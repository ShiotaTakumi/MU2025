// JSON ファイルを読み込んで、グラフ要素を初期化
// Load the JSON file and initialize graph elements
fetch('json/sample.json')
// JSON として読み込む
// Parse response as JSON
  .then(response => response.json())
  .then(data => {
    // 各ノードに label を追加（ここでは ID を使う）
    // Add label field to each node (using ID as label)
    data.nodes.forEach(node => {
      node.data.label = node.data.id;
    });

    // Cytoscape.js の初期化
    // Initialize Cytoscape.js
    window.cy = cytoscape({
      // 描画対象の DOM 要素を指定
      // Specify container DOM element
      container: document.getElementById('cy'),

      // JSON から読み込んだ頂点と辺情報をセット
      // Set nodes and edges from loaded JSON
      elements: data,

      minZoom: 0.5, // ズームアウトの下限 / Minimum zoom level
      maxZoom: 2,   // ズームインの上限 / Maximum zoom level

      // スタイル設定（頂点・辺）
      // Style settings (nodes and edges)
      style: [
        {
          // 頂点のスタイル指定
          // Node styling
          selector: 'node',
          style: {
            'width': '12px',             // 頂点の幅 / Node width
            'height': '12px',            // 頂点の高さ / Node height
            'background-color': '#000',  // 頂点の色（黒）/ Node color (black)
            'label': 'data(label)',      // ラベルをノードデータの label 属性から表示 / Show label from node's data.label
            'font-size': '18px'          // ラベルのフォントサイズを設定 / Set font size for the label
          }
        },
        {
          // 辺のスタイル指定
          // Edge styling
          selector: 'edge',
          style: {
            'width': 1,               // 線の太さ / Line thickness
            'line-color': '#000'      // 線の色（黒）/ Line color (black)
          }
        }
      ]
    });
  });