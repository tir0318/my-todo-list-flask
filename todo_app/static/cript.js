document.addEventListener('DOMContentLoaded', () => {

    // 削除ボタンに確認機能を追加
    const deleteButtons = document.querySelectorAll('.delete-confirm');

    deleteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            // "本当に削除しますか？" という確認ダイアログを表示
            const isConfirmed = confirm('Are you sure you want to delete this task?');

            // ユーザーが "キャンセル" を押した場合
            if (!isConfirmed) {
                // リンクの遷移をキャンセル
                event.preventDefault();
            }
        });
    });

    // 新規タスク入力フォームに自動でフォーカスを当てる
    const newTaskInput = document.querySelector('.add-form input[name="task"]');
    if (newTaskInput) {
        newTaskInput.focus();
    }

});