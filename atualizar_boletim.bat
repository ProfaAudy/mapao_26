@echo off
:: Configura o console do Windows para exibir caracteres especiais (acentuação) corretamente
chcp 65001 > nul

echo ====================================================
echo   SISTEMA DE BOLETIM: ATUALIZAÇÃO E ENVIO AO GITHUB
echo ====================================================
echo.

:: 1. Executa a extração dos dados locais com o script Python
echo [1/3] Processando arquivos Excel na pasta 'sources'...
python "%~dp0scripts\extract_data.py"
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERRO] Falha ao processar as notas no script Python.
    echo A operação foi cancelada. Verifique as mensagens de erro acima.
    goto error
)
echo [OK] Extração concluída com sucesso!
echo.

:: 2. Faz commit e envia as alterações ao GitHub
echo [2/3] Verificando se há novas notas ou arquivos para enviar ao GitHub...

:: Verifica se houve alteração em data/data.js ou na pasta sources
git status --porcelain "%~dp0data\data.js" "%~dp0sources" | findstr /R "." > nul
if %ERRORLEVEL% neq 0 (
    echo [INFO] Nenhuma nova alteração detectada em data/data.js ou sources/.
    echo Nada novo para enviar ao GitHub.
    goto success
)

echo.
echo [3/3] Enviando atualizações ao repositório GitHub...
git add "%~dp0data\data.js" "%~dp0sources"
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Erro ao preparar arquivos com 'git add'.
    goto error
)

git commit -m "Atualização automática de notas e boletins via script"
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Erro ao realizar o commit.
    goto error
)

git push origin main
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERRO] Falha ao enviar para o GitHub (git push).
    echo Verifique sua conexão de internet e permissões de acesso ao repositório.
    goto error
)

:success
echo.
echo ====================================================
echo   SUCESSO! O processo foi concluído com êxito.
echo ====================================================
echo O boletim está atualizado e publicado no GitHub.
goto end

:error
echo.
echo ====================================================
echo   FALHA! O processo não pôde ser concluído.
echo ====================================================
echo Algumas etapas falharam. Veja os erros acima.

:end
echo.
pause
