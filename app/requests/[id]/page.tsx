import { PageShell } from '@/components/page-shell';

type RequestDetailsPageProps = {
  params: Promise<{
    id: string;
  }>;
};

export default async function RequestDetailsPage({ params }: RequestDetailsPageProps) {
  const { id } = await params;

  return (
    <PageShell
      title={`Заявка #${id}`}
      description="Карточка заявки с детальной информацией. Бизнес-логика будет добавлена в следующих итерациях."
    />
  );
}
