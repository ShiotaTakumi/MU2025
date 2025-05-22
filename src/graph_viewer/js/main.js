// js/main.js

// JSON ディレクトリ構造に合わせて、選択肢を定義
// Define the selection options based on the JSON directory structure
const dataMap = {
  polyhedron: {
    n4: Array.from({ length: 1 }, (_, i) => `${i + 1}.json`),
    n5: Array.from({ length: 2 }, (_, i) => `${i + 1}.json`),
    n6: Array.from({ length: 7 }, (_, i) => `${i + 1}.json`),
    n7: Array.from({ length: 34 }, (_, i) => `${i + 1}.json`),
    n8: Array.from({ length: 257 }, (_, i) => `${i + 1}.json`),
    n9: Array.from({ length: 2606 }, (_, i) => `${i + 1}.json`)
  },
  pyramid: {
    n4: ['1.json'],
    n5: ['1.json'],
    n6: ['1.json'],
    n7: ['1.json'],
    n8: ['1.json'],
    n9: ['1.json'],
    n10: ['1.json'],
    n11: ['1.json']
  },
  bipyramid: {
    n5: ['1.json'],
    n6: ['1.json'],
    n7: ['1.json'],
    n8: ['1.json'],
    n9: ['1.json'],
    n10: ['1.json'],
    n11: ['1.json']
  }
};

// Cytoscape インスタンスとオリジナル要素を保存する変数
// Variables to hold the Cytoscape instance and the original elements for reset
let cyInstance = null;
let originalElements = null;

// グラフを読み込んで描画する関数
// Function to load a JSON graph and render it with Cytoscape
function loadGraph(path) {
  console.log('[loadGraph] fetching:', path);

  // 既に Cytoscape インスタンスがあれば破棄
  // If a Cytoscape instance already exists, destroy it before creating a new one
  if (cyInstance && typeof cyInstance.destroy === 'function') {
    cyInstance.destroy();
    cyInstance = null;
  }

  // 指定されたパスの JSON ファイルを取得
  // Fetch the JSON file from the specified path
  fetch(path)
    .then(response => {
      // HTTP レスポンスが OK でなければ例外を投げる
      // Throw an error if the HTTP response is not OK
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(data => {
      // 取得したデータをディープコピーして保持（リセット用）
      // Deep-copy the fetched data for resetting later
      originalElements = JSON.parse(JSON.stringify({
        nodes: data.nodes,
        edges: data.edges
      }));

      // Cytoscape インスタンスを生成
      // Create a new Cytoscape instance and render the graph
      cyInstance = cytoscape({
        container: document.getElementById('cy'),
        elements: {
          nodes: data.nodes,
          edges: data.edges
        },
        layout: { name: 'preset' },
        minZoom: 0.5,  // ズームアウトの下限 / Minimum zoom level
        maxZoom: 2,    // ズームインの上限 / Maximum zoom level
        style: [
          {
            selector: 'node',
            style: {
              width: '12px',               // ノード幅 / Node width
              height: '12px',              // ノード高さ / Node height
              'background-color': '#000',  // ノード色（黒）/ Node color (black)
              label: 'data(label)',        // ラベルに data.label を表示 / Show data.label as node label
              'font-size': '18px'          // ラベルフォントサイズ / Label font size
            }
          },
          {
            selector: 'edge',
            style: {
              width: 1.5,                  // エッジ幅 / Edge width
              'line-color': '#000'         // エッジ色（黒）/ Edge color (black)
            }
          },
          {
            selector: 'edge[highlighted = "true"]',
            style: {
              width: 1.3,                  // 強調エッジ幅 / Highlighted edge width
              'line-color': '#303030',     // 強調エッジ色（灰色）/ Highlighted edge color (gray)
              'line-style': 'dashed',      // 点線スタイル / Dashed line style
              'line-dash-pattern': [6, 3]  // 点線の長さと間隔 / Dash length and gap
            }
          }
        ]
      });

      // 辺クリックでハイライト切替
      // Toggle edge highlight on click
      cyInstance.on('tap', 'edge', evt => {
        const e = evt.target;
        const currently = e.data('highlighted') === 'true';
        e.data('highlighted', currently ? 'false' : 'true');
      });
    })
    .catch(err => {
      // エラー発生時にコンソールとアラートに出力
      // Log and alert on error
      console.error('[loadGraph] error:', err);
      alert('グラフの読み込みに失敗しました: ' + err.message);
    });
}

// グラフを中央に配置する関数
// Function to re-layout and center the graph
function centering() {
  if (!cyInstance) return;
  cyInstance.layout({ name: 'preset' }).run();  // 再配置 / Re-run layout
  cyInstance.center();                           // 中央にパン / Center view
}

// ページ読み込み後に初期化＆イベント登録
// Initialize on page load and set up event listeners
window.onload = () => {
  // セレクトボックスとボタンの要素を取得
  // Get references to select boxes and draw button
  const typeSelect = document.getElementById('typeSelect');
  const nSelect    = document.getElementById('nSelect');
  const fileSelect = document.getElementById('fileSelect');
  const drawBtn    = document.getElementById('drawBtn');

  // fileSelect を更新する関数
  // Function to update the file list based on current type and n selection
  const updateFileOptions = () => {
    fileSelect.innerHTML = '';  // 既存オプションをクリア / Clear existing options
    dataMap[typeSelect.value][nSelect.value].forEach(f => {
      const opt = document.createElement('option');
      opt.value = f;
      opt.textContent = f;
      fileSelect.appendChild(opt);
    });
  };

  // nSelect を更新する関数
  // Function to update the n list based on current type selection
  const updateNOptions = () => {
    nSelect.innerHTML = '';  // 既存オプションをクリア / Clear existing options
    Object.keys(dataMap[typeSelect.value]).forEach(n => {
      const opt = document.createElement('option');
      opt.value = n;
      opt.textContent = n;
      nSelect.appendChild(opt);
    });
    updateFileOptions();  // ファイルオプションも更新 / Also update file options
  };

  // typeSelect による nSelect 更新イベント
  // Update n options when the type selection changes
  typeSelect.addEventListener('change', updateNOptions);
  // nSelect による fileSelect 更新イベント
  // Update file options when the n selection changes
  nSelect.addEventListener('change', updateFileOptions);

  // Draw ボタン押下時の処理
  // On Draw button click, construct path and load graph
  drawBtn.addEventListener('click', () => {
    const path = `json/${typeSelect.value}/${nSelect.value}/${fileSelect.value}`;
    console.log('[Draw] path=', path);
    loadGraph(path);
  });

  // 初期描画のための初期オプション設定とロード
  // Set initial options and perform first graph load
  // 初期の type と n のオプションを生成 / Populate initial type and n options
  Object.keys(dataMap).forEach(t => {
    const opt = document.createElement('option');
    opt.value = t;
    opt.textContent = t;
    typeSelect.appendChild(opt);
  });
  updateNOptions();  // n と file のオプションも初期化 / Initialize n and file options

  // 初回ロード / Initial load
  const initPath = `json/${typeSelect.value}/${nSelect.value}/${fileSelect.value}`;
  console.log('[Init] path=', initPath);
  loadGraph(initPath);
};