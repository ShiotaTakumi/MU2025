// JSON ファイルを読み込んで、グラフ要素を初期化
// Load the JSON file and initialize graph elements
fetch('json/sample.json')
// JSON として読み込む
// Parse response as JSON
  .then(response => response.json())
  .then(data => {
    // 元のデータをディープコピーでグローバル変数として保持
    // Deep copy original data to store globally for resetting
    window.originalElements = JSON.parse(JSON.stringify({
      nodes: data.nodes,
      edges: data.edges
    }));

    // Cytoscape.js の初期化
    // Initialize Cytoscape.js
    window.cy = cytoscape({
      // 描画対象の DOM 要素を指定
      // Specify container DOM element
      container: document.getElementById('cy'),

      // JSON から読み込んだ頂点と辺情報をセット
      // Set nodes and edges from loaded JSON
      elements: {
        nodes: data.nodes,
        edges: data.edges
      },

      // ノードの位置を JSON の position に従って固定
      // Fix node positions based on JSON position
      layout: {
        name: 'preset'
      },

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
          // 通常の辺のスタイル
          // Default edge styling
          selector: 'edge',
          style: {
            'width': 1.5,
            'line-color': '#000'         // 線の色（黒）/ Line color (black)
          }
        },
        {
          // 強調表示された辺のスタイル
          // Highlighted edge styling
          selector: 'edge[highlighted = "true"]',
          style: {
            'width': 1.3,
            'line-color': '#303030',     // 線の色（灰色）/ Line color (gray)
            'line-style': 'dashed',      // 点線に変更 / Make it dashed
            'line-dash-pattern': [6, 3]  // 点線の長さと間隔 / [dash length, gap]
          }
        }
      ]
    });

    // 辺クリック時に色をトグルするイベント追加
    // Add click event to toggle edge color
    window.cy.on('tap', 'edge', function (evt) {
      const edge = evt.target;
      const isHighlighted = edge.data('highlighted') === 'true';
      edge.data('highlighted', isHighlighted ? 'false' : 'true');
    });
  });

// リセットボタン用関数：位置・ズーム・パンをすべて元に戻す
// Reset to original preset layout, zoom, and pan
function resetLayout() {
  if (window.cy && window.originalElements) {
    // 既存の要素を削除
    // Remove current elements
    window.cy.elements().remove();

    // ディープコピーで初期データを再複製
    // Deep copy original elements
    const resetElements = JSON.parse(JSON.stringify(window.originalElements));

    // ノードの位置を強制的にセット
    // Re-add nodes with positions
    resetElements.nodes.forEach(node => {
      window.cy.add({
        group: 'nodes',
        data: node.data,
        position: node.position
      });
    });

    // エッジを再追加（highlighted 状態を false に初期化）
    // Re-add edges with no highlight
    resetElements.edges.forEach(edge => {
      window.cy.add({
        group: 'edges',
        data: {
          ...edge.data,
          highlighted: 'false' // リセット時に必ず false に / Always reset to false
        }
      });
    });

    // preset レイアウト（位置は既に含まれているが、念のため実行）
    // Run preset layout (though positions are already set)
    const layout = window.cy.layout({ name: 'preset' });
    layout.run();

    // グラフの中央にパンする
    // Center the graph view
    window.cy.center();
  }
}